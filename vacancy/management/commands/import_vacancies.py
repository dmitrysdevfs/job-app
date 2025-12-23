import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from vacancy.models import Vacancy
from employer.models import Employer
from dictionary.models import VacancySource, EmploymentType, EducationLevel, Degree
from position.models import JobTitle
from location.models import Settlement, CityDistrict
from kved.models import Class as KvedClass

class Command(BaseCommand):
    help = 'Імпорт вакансій з CSV файлу'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Шлях до CSV файлу')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'Файл не знайдено: {csv_file_path}'))
            return

        # Знаходимо дефолтне джерело (ДСЗ)
        default_source, _ = VacancySource.objects.get_or_create(
            code='dsz', 
            defaults={'name': 'Державна служба зайнятості'}
        )
        
        # Дефолтні типи (якщо вони будуть потрібні)
        default_employment = EmploymentType.objects.first()
        default_education = EducationLevel.objects.first()

        with open(csv_file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            
            created_count = 0
            updated_count = 0
            error_count = 0

            for row in reader:
                tax_id = row.get('employer_tax_id', '').strip()
                external_id = row.get('external_id', '').strip()
                pos_code = row.get('position_code', '').strip()
                loc_code = row.get('location_code', '').strip()
                salary_min = row.get('salary_min', '').strip()
                salary_max = row.get('salary_max', '').strip()
                description = row.get('description', '').strip()
                report_3pn = row.get('report_3pn_date', '').strip()
                published_at = row.get('published_at', '').strip()
                edu_name = row.get('education_level', '').strip()
                deg_name = row.get('degree', '').strip()
                confirmed_at = row.get('confirmed_at', '').strip()

                if not tax_id or not pos_code or not loc_code:
                    self.stdout.write(self.style.WARNING(f'Пропущено рядок: недостатньо даних ({row})'))
                    error_count += 1
                    continue

                # Пошук Роботодавця
                employer = Employer.objects.filter(tax_id=tax_id).first()
                if not employer:
                    self.stdout.write(self.style.WARNING(f'Роботодавця з tax_id {tax_id} не знайдено. Пропуск.'))
                    error_count += 1
                    continue

                # Пошук Посади
                position = JobTitle.objects.filter(code=pos_code).first()
                if not position:
                    self.stdout.write(self.style.WARNING(f'Посаду {pos_code} не знайдено. Пропуск.'))
                    error_count += 1
                    continue

                # Пошук Локації (з підтримкою районів у місті)
                location = Settlement.objects.filter(code=loc_code).first()
                if not location:
                    city_district = CityDistrict.objects.filter(code=loc_code).select_related('settlement').first()
                    if city_district:
                        location = city_district.settlement
                
                if not location:
                    self.stdout.write(self.style.WARNING(f'Локацію {loc_code} не знайдено. Пропуск.'))
                    error_count += 1
                    continue

                # Пошук додаткових довідників
                education = EducationLevel.objects.filter(name__iexact=edu_name).first() if edu_name else default_education
                degree = Degree.objects.filter(name__iexact=deg_name).first() if deg_name else None

                # Обробка зарплати (Логіка користувача: якщо min пуста, то min = max)
                try:
                    s_max = int(salary_max) if salary_max else None
                    s_min = int(salary_min) if salary_min else s_max
                except ValueError:
                    s_min = s_max = None

                # Парсинг дат
                def parse_date(date_str, is_datetime=False):
                    if not date_str: return None
                    try:
                        dt = datetime.strptime(date_str, '%d.%m.%Y')
                        return timezone.make_aware(dt) if is_datetime else dt.date()
                    except ValueError:
                        return None

                r_date = parse_date(report_3pn)
                p_date = parse_date(published_at, is_datetime=True) or timezone.now()
                c_date = parse_date(confirmed_at, is_datetime=True)

                try:
                    vacancy, created = Vacancy.objects.update_or_create(
                        external_id=external_id,
                        defaults={
                            'employer': employer,
                            'title': position.name,  # Беремо назву з довідника
                            'position': position,
                            'location': location,
                            'salary_min': s_min,
                            'salary_max': s_max,
                            'description': description or position.name,
                            'report_3pn_date': r_date,
                            'published_at': p_date,
                            'confirmed_at': c_date,
                            'source': default_source,
                            'employment_type': default_employment,
                            'education_level': education,
                            'degree': degree,
                        }
                    )
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Помилка при імпорті {external_id}: {str(e)}'))
                    error_count += 1

            self.stdout.write(self.style.SUCCESS(
                f'Імпорт вакансій завершено. Створено: {created_count}, Оновлено: {updated_count}, Помилок: {error_count}'
            ))
