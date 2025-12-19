from django.db import models


class Section(models.Model):
    """
    Розділ: Top level category (e.g., "1" - Законодавці...)
    """
    code = models.CharField(max_length=20, unique=True, verbose_name="Код КП")
    name = models.CharField(max_length=512, verbose_name="Назва")

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Розділ"
        verbose_name_plural = "Розділи"
        ordering = ['code']


class Subsection(models.Model):
    """
    Підрозділ: Optional intermediate level (e.g., "11", "12")
    """
    code = models.CharField(max_length=20, unique=True, verbose_name="Код КП")
    name = models.CharField(max_length=512, verbose_name="Назва")
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='subsections',
        verbose_name="Розділ"
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Підрозділ"
        verbose_name_plural = "Підрозділи"
        ordering = ['code']


class Class(models.Model):
    """
    Клас: Main grouping (e.g., "111", "112")
    """
    code = models.CharField(max_length=20, unique=True, verbose_name="Код КП")
    name = models.CharField(max_length=512, verbose_name="Назва")
    subsection = models.ForeignKey(
        Subsection,
        on_delete=models.CASCADE,
        related_name='classes',
        null=True,
        blank=True,
        verbose_name="Підрозділ"
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='classes',
        verbose_name="Розділ"
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Клас"
        verbose_name_plural = "Класи"
        ordering = ['code']


class Subclass(models.Model):
    """
    Підклас: Specific grouping (e.g., "1110", "1120")
    """
    code = models.CharField(max_length=20, unique=True, verbose_name="Код КП")
    name = models.CharField(max_length=512, verbose_name="Назва")
    class_obj = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='subclasses',
        verbose_name="Клас"
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Підклас"
        verbose_name_plural = "Підкласи"
        ordering = ['code']


class Group(models.Model):
    """
    Група: Detailed grouping (e.g., "1120" without dot, if it has children with dots)
    Note: Some 4-digit codes might be Groups if they have Position children
    """
    code = models.CharField(max_length=20, unique=True, verbose_name="Код КП")
    name = models.CharField(max_length=512, verbose_name="Назва")
    class_obj = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='groups',
        null=True,
        blank=True,
        verbose_name="Клас"
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Група"
        verbose_name_plural = "Групи"
        ordering = ['code']


class Position(models.Model):
    """
    Професійна назва роботи: The leaf node (e.g., "1120.1", "1120.2")
    Position always belongs to a Group (which may have been converted from Subclass)
    """
    code = models.CharField(max_length=20, db_index=True, verbose_name="Код КП")
    name = models.CharField(max_length=512, verbose_name="Назва")
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name="Група"
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Професійна назва роботи"
        verbose_name_plural = "Професійні назви робіт"
        ordering = ['code']


class JobTitle(models.Model):
    """
    Детальна назва роботи (з додатку Б, розширений список).
    Може посилатись на Position, Group, або Subclass, залежно від того, що є 'батьком' у коді.
    """
    code = models.CharField(max_length=20, db_index=True, verbose_name="Код КП")
    name = models.CharField(max_length=512, verbose_name="Професійна назва роботи")
    
    # Extra codes from mapping
    zkpptr_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Код ЗКППТР")
    etkd_issue = models.CharField(max_length=20, blank=True, null=True, verbose_name="Випуск ЄТКД")
    dkhp_issue = models.CharField(max_length=20, blank=True, null=True, verbose_name="Випуск ДКХП")
    
    # Hierarchy links - mutually exclusive ideally, but we'll try to match best fit
    position = models.ForeignKey(
        Position, 
        on_delete=models.CASCADE, 
        related_name='job_titles', 
        null=True, 
        blank=True,
        verbose_name="Професійна назва (КП)"
    )
    group = models.ForeignKey(
        Group, 
        on_delete=models.CASCADE, 
        related_name='job_titles', 
        null=True, 
        blank=True,
        verbose_name="Група (КП)"
    )
    subclass = models.ForeignKey(
        Subclass, 
        on_delete=models.CASCADE, 
        related_name='job_titles', 
        null=True, 
        blank=True,
        verbose_name="Підклас (КП)"
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Детальна назва роботи"
        verbose_name_plural = "Детальні назви робіт"
        ordering = ['code', 'name']
