from functools import partial
from django.db import models
from core.utils import upload_to
from django.conf import settings
from django.core.validators import RegexValidator


class Employer(models.Model):
    """Профіль роботодавця (Юридична особа, ФОП тощо)"""
    
    EMPLOYER_TYPE_CHOICES = (
        ('LEGAL', 'Юридична особа'),
        ('FOP', 'ФОП'),
        ('SELF', 'Самозайнятий'),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employers',
        verbose_name="Власник профілю"
    )
    name = models.CharField(
        max_length=255, 
        verbose_name="Офіційна назва / ПІБ"
    )
    brand_name = models.CharField(
        max_length=255, 
        blank=True, 
        default="",
        verbose_name="Бренд / Публічна назва"
    )
    tax_id = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{8,10}$', 'Код повинен містити 8 (ЄДРПОУ) або 10 (РНОКПП) цифр')],
        verbose_name="ЄДРПОУ / РНОКПП"
    )
    employer_type = models.CharField(
        max_length=10, 
        choices=EMPLOYER_TYPE_CHOICES, 
        default='LEGAL',
        verbose_name="Тип роботодавця"
    )
    kved = models.ForeignKey(
        'kved.Class', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='employers',
        verbose_name="Основний КВЕД"
    )
    location = models.ForeignKey(
        'location.Settlement', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='employers',
        verbose_name="Місцезнаходження"
    )
    description = models.TextField(
        blank=True, 
        default="",
        verbose_name="Про роботодавця"
    )
    website = models.URLField(
        blank=True, 
        default="",
        verbose_name="Веб-сайт"
    )
    address = models.CharField(
        max_length=255, 
        blank=True, 
        default="", 
        verbose_name="Юридична адреса / Офіс"
    )
    logo = models.ImageField(
        upload_to=partial(upload_to, folder_name='employer_logos'), 
        null=True, 
        blank=True, 
        verbose_name="Логотип"
    )
    is_verified = models.BooleanField(
        default=False, 
        verbose_name="Перевірено адміністратором"
    )
    staff = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='employer_staff',
        verbose_name="Персонал / Рекрутери"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name = "Роботодавець"
        verbose_name_plural = "Роботодавці"
        ordering = ['name']

    def __str__(self):
        return self.brand_name if self.brand_name else self.name
