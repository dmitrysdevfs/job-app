import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from employer.models import Employer
from kved.models import Class as KvedClass
from location.models import Settlement, CityDistrict

User = get_user_model()

class Command(BaseCommand):
    help = 'Імпорт роботодавців з CSV файлу'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Шлях до CSV файлу')
        parser.add_argument('--owner', type=str, help='Email власника для всіх роботодавців (за замовчуванням: admin@admin.admin)')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        owner_email = options.get('owner') or 'admin@admin.admin'

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'Файл не знайдено: {csv_file_path}'))
            return

        try:
            owner = User.objects.get(email=owner_email)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Користувача з email {owner_email} не знайдено.'))
            return

        with open(csv_file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f, delimiter=';')
            
            created_count = 0
            updated_count = 0
            error_count = 0

            for row in reader:
                tax_id = row.get('tax_id', '').strip()
                name = row.get('name', '').strip()
                kved_code = row.get('kved_code', '').strip()
                settlement_code = row.get('settlement_code', '').strip()
                address = row.get('address', '').strip()

                if not tax_id or not name:
                    self.stdout.write(self.style.WARNING(f'Пропущено рядок: відсутній tax_id або name ({row})'))
                    error_count += 1
                    continue

                # Пошук КВЕД
                kved = None
                if kved_code:
                    kved = KvedClass.objects.filter(code=kved_code).first()
                    if not kved:
                        self.stdout.write(self.style.WARNING(f'КВЕД {kved_code} не знайдено для {tax_id}'))

                # Пошук населеного пункту
                location = None
                if settlement_code:
                    location = Settlement.objects.filter(code=settlement_code).first()
                    if not location:
                        # Можливо, це код району в місті (B)?
                        city_district = CityDistrict.objects.filter(code=settlement_code).select_related('settlement').first()
                        if city_district:
                            location = city_district.settlement
                    
                    if not location:
                        self.stdout.write(self.style.WARNING(f'Населений пункт або район мiста {settlement_code} не знайдено для {tax_id}'))

                try:
                    employer, created = Employer.objects.update_or_create(
                        tax_id=tax_id,
                        defaults={
                            'name': name,
                            'owner': owner,
                            'kved': kved,
                            'location': location,
                            'address': address,
                        }
                    )
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Помилка при імпорті {tax_id}: {str(e)}'))
                    error_count += 1

            self.stdout.write(self.style.SUCCESS(
                f'Імпорт завершено. Створено: {created_count}, Оновлено: {updated_count}, Помилок: {error_count}'
            ))
