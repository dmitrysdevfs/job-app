from django.db import models
from django.utils.translation import gettext_lazy as _


class Vacancy(models.Model):
    """Модель вакансії"""

    CURRENCY_CHOICES = (
        ('UAH', '₴ (Гривня)'),
        ('USD', '$ (Долар США)'),
        ('EUR', '€ (Євро)'),
    )

    # Core Info
    employer = models.ForeignKey(
        'employer.Employer',
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name="Роботодавець"
    )
    title = models.CharField(max_length=255, verbose_name="Назва вакансії")
    description = models.TextField(verbose_name="Опис вакансії")
    requirements = models.TextField(blank=True, default="", verbose_name="Вимоги")
    responsibilities = models.TextField(blank=True, default="", verbose_name="Обов'язки")

    # Categorization (Dictionaries)
    position = models.ForeignKey(
        'position.JobTitle',
        on_delete=models.PROTECT,
        related_name='vacancies',
        verbose_name="Посада (Детальна назва)"
    )
    speciality = models.ForeignKey(
        'speciality.Speciality',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vacancies',
        verbose_name="Спеціальність"
    )
    kved = models.ForeignKey(
        'kved.Class',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vacancies',
        verbose_name="Вид діяльності (КВЕД)"
    )
    location = models.ForeignKey(
        'location.Settlement',
        on_delete=models.PROTECT,
        related_name='vacancies',
        verbose_name="Місце роботи (Населений пункт)"
    )

    # Auxiliary Dictionaries
    employment_type = models.ForeignKey(
        'dictionary.EmploymentType',
        on_delete=models.PROTECT,
        verbose_name="Вид зайнятості"
    )
    education_level = models.ForeignKey(
        'dictionary.EducationLevel',
        on_delete=models.PROTECT,
        verbose_name="Рівень освіти"
    )
    degree = models.ForeignKey(
        'dictionary.Degree',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Освітній ступінь"
    )
    tags = models.ManyToManyField(
        'dictionary.Tag',
        blank=True,
        related_name='vacancies',
        verbose_name="Теги / Ознаки"
    )

    # Conditions
    salary_min = models.PositiveIntegerField(null=True, blank=True, verbose_name="Зарплата від")
    salary_max = models.PositiveIntegerField(null=True, blank=True, verbose_name="Зарплата до")
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='UAH',
        verbose_name="Валюта"
    )

    # Metadata
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    published_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публікації")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Термін дії до")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    class Meta:
        verbose_name = "Вакансія"
        verbose_name_plural = "Вакансії"
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.title} @ {self.employer.brand_name or self.employer.name}"
