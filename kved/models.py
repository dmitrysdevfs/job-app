from django.db import models

class Section(models.Model):
    code = models.CharField(max_length=1, unique=True, db_index=True, verbose_name="Код")
    name = models.CharField(max_length=255, verbose_name="Назва")

    class Meta:
        verbose_name = "Секція"
        verbose_name_plural = "Секції"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"

class Division(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="divisions", verbose_name="Секція")
    code = models.CharField(max_length=2, unique=True, db_index=True, verbose_name="Код")
    name = models.CharField(max_length=255, verbose_name="Назва")

    class Meta:
        verbose_name = "Розділ"
        verbose_name_plural = "Розділи"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"

class Group(models.Model):
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name="groups", verbose_name="Розділ")
    code = models.CharField(max_length=10, unique=True, db_index=True, verbose_name="Код")
    name = models.CharField(max_length=255, verbose_name="Назва")

    class Meta:
        verbose_name = "Група"
        verbose_name_plural = "Групи"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"

class Class(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="classes", verbose_name="Група")
    code = models.CharField(max_length=10, unique=True, db_index=True, verbose_name="Код")
    name = models.CharField(max_length=255, verbose_name="Назва")

    class Meta:
        verbose_name = "Клас"
        verbose_name_plural = "Класи"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"
