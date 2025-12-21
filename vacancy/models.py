from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class Vacancy(models.Model):
    """Модель вакансії"""

    CURRENCY_CHOICES = (
        ('UAH', '₴ (Гривня)'),
        ('USD', '$ (Долар США)'),
        ('EUR', '€ (Євро)'),
    )

    STATUS_CHOICES = (
        ('active', 'Активна'),
        ('filled', 'Укомплектована'),
        ('withdrawn', 'Скасована (відсутність потреби)'),
        ('expired', 'Протермінована (архів)'),
    )

    # Core Info
    employer = models.ForeignKey(
        'employer.Employer',
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name="Роботодавець"
    )
    title = models.CharField(max_length=255, verbose_name="Назва вакансії")
    
    # External Integration
    external_id = models.CharField(
        max_length=50, 
        unique=True, 
        null=True, 
        blank=True, 
        verbose_name="Внутрішній номер (ID)",
        validators=[
            RegexValidator(
                regex=r'^\d{14}$',
                message="ID повинен складатися з 14 цифр (Центр + Дата + Номер)"
            )
        ]
    )
    source = models.ForeignKey(
        'dictionary.VacancySource',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vacancies',
        verbose_name="Джерело"
    )
    report_3pn_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Дата звіту 3-ПН"
    )
    address = models.CharField(
        max_length=255, 
        blank=True, 
        default="", 
        verbose_name="Адреса (вулиця, будинок)"
    )

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
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active', 
        verbose_name="Статус"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна (публічна)")
    published_at = models.DateTimeField(default=timezone.now, verbose_name="Дата публікації")
    confirmed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата підтвердження")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата закриття")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Термін дії до")
    
    # Continuity & History
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='republications',
        verbose_name="Попередня вакансія (ланцюжок)"
    )
    generation = models.PositiveIntegerField(default=1, verbose_name="Покоління")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    def save(self, *args, **kwargs):
        # Автоматичний розрахунок покоління
        if self.parent:
            self.generation = self.parent.generation + 1
        
        # Автоматична дата закриття
        if self.status != 'active' and not self.closed_at:
            self.closed_at = timezone.now()
        elif self.status == 'active':
            self.closed_at = None

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Вакансія"
        verbose_name_plural = "Вакансії"
        ordering = ['-published_at']

    def __str__(self):
        return f"{self.title} @ {self.employer.brand_name or self.employer.name}"
