import os
from django.core.management.base import BaseCommand
from dictionary.models import EmploymentType, EducationLevel, Degree, Tag


class Command(BaseCommand):
    help = 'Заповнює допоміжні довідники початковими даними'

    def handle(self, *args, **options):
        # 1. EmploymentType
        employment_types = [
            "Повна зайнятість",
            "Часткова зайнятість",
            "Дистанційна робота",
            "Гібридний формат",
            "Проєктна робота / Freelance",
            "Стажування",
        ]
        for idx, name in enumerate(employment_types):
            obj, created = EmploymentType.objects.get_or_create(name=name, defaults={'order': idx})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Створено вид зайнятості: {name}'))

        # 2. EducationLevel
        education_levels = [
            "Загальна середня",
            "Професійно-технічна",
            "Неповна вища",
            "Базова вища",
            "Вища освіта",
        ]
        for idx, name in enumerate(education_levels):
            obj, created = EducationLevel.objects.get_or_create(name=name, defaults={'order': idx})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Створено рівень освіти: {name}'))

        # 3. Degree
        degrees = [
            "Кваліфікований робітник",
            "Молодший бакалавр",
            "Фаховий молодший бакалавр",
            "Молодший спеціаліст",
            "Бакалавр",
            "Спеціаліст",
            "Магістр",
            "Кандидат наук",
            "Доктор наук",
        ]
        for idx, name in enumerate(degrees):
            obj, created = Degree.objects.get_or_create(name=name, defaults={'order': idx})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Створено ступінь: {name}'))

        # 4. Tag
        tags = [
            "Державна служба",
            "Вакансія з житлом",
            "Для ветеранів",
            "Перша робота / Без досвіду",
            "Робота для студентів",
            "Для осіб з інвалідністю",
            "Бронювання працівників",
        ]
        for idx, name in enumerate(tags):
            obj, created = Tag.objects.get_or_create(name=name, defaults={'order': idx})
            if created:
                self.stdout.write(self.style.SUCCESS(f'Створено тег: {name}'))

        self.stdout.write(self.style.SUCCESS('Всі довідники успішно оновлено!'))
