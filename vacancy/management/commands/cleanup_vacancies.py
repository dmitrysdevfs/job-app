from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from vacancy.models import Vacancy


class Command(BaseCommand):
    help = 'Автоматичне закриття вакансій, старших за 90 днів'

    def handle(self, *args, **options):
        threshold_date = timezone.now() - timedelta(days=90)
        
        # Шукаємо активні вакансії, створені більше 90 днів тому
        old_vacancies = Vacancy.objects.filter(
            is_active=True,
            created_at__lt=threshold_date
        )
        
        count = old_vacancies.count()
        
        if count > 0:
            # Деактивуємо їх
            old_vacancies.update(is_active=False)
            self.stdout.write(
                self.style.SUCCESS(f'Успішно деактивовано {count} старих вакансій.')
            )
        else:
            self.stdout.write(
                self.style.NOTICE('Застарілих вакансій не знайдемо.')
            )
