from functools import partial
from django.db import models
from core.utils import upload_to


class EmploymentType(models.Model):
    """Вид зайнятості (Повна, Часткова тощо)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Вид зайнятості"
        verbose_name_plural = "Види зайнятості"

    def __str__(self):
        return self.name


class EducationLevel(models.Model):
    """Рівень освіти (Повна вища, Базова вища тощо)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Рівень освіти"
        verbose_name_plural = "Рівні освіти"

    def __str__(self):
        return self.name


class Degree(models.Model):
    """Освітньо-кваліфікаційний ступінь (Кваліфікований робітник, Бакалавр, Магістр, Кандидат наук, Доктор наук тощо)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Освітній ступінь"
        verbose_name_plural = "Освітні ступені"

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Тег / Ознака (Державна служба, Вакансія з житлом тощо)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    icon = models.ImageField(
        upload_to=partial(upload_to, folder_name='tag_icons'), 
        null=True, 
        blank=True, 
        verbose_name="Іконка / Логотип"
    )
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class VacancySource(models.Model):
    """Джерело вакансії (ДСЗ, Work.ua, robota.ua тощо)"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва")
    code = models.SlugField(max_length=50, unique=True, verbose_name="Системний код")
    icon = models.ImageField(
        upload_to=partial(upload_to, folder_name='source_icons'),
        null=True,
        blank=True,
        verbose_name="Іконка / Логотип"
    )
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Джерело вакансій"
        verbose_name_plural = "Джерела вакансій"

    def __str__(self):
        return self.name
