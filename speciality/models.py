from django.db import models
from django.core.validators import RegexValidator


class KnowledgeField(models.Model):
    """Галузь знань (01, 02, 03...)"""
    code = models.CharField(
        max_length=2,
        unique=True,
        validators=[RegexValidator(r'^\d{2}$', 'Code must be 2 digits')]
    )
    name = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    # TODO: Додати версійність пізніше
    # version = models.ForeignKey('ClassificationVersion', ...)

    class Meta:
        ordering = ['order', 'code']
        verbose_name = "Knowledge Field"
        verbose_name_plural = "Knowledge Fields"

    def __str__(self):
        return f"{self.code} - {self.name}"


class Speciality(models.Model):
    """Спеціальність (011, 012, 013...)"""
    knowledge_field = models.ForeignKey(
        KnowledgeField,
        on_delete=models.CASCADE,
        related_name='specialities'
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        validators=[RegexValidator(r'^\d{3,10}$', 'Code must be 3-10 digits')]
    )
    name = models.CharField(max_length=300)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    level = models.IntegerField(default=1)
    order = models.IntegerField(default=0)

    # TODO: Додати версійність пізніше
    # version = models.ForeignKey('ClassificationVersion', ...)

    class Meta:
        ordering = ['knowledge_field', 'level', 'order', 'code']
        verbose_name = "Speciality"
        verbose_name_plural = "Specialities"
        indexes = [
            models.Index(fields=['knowledge_field', 'code']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_full_path(self):
        """Повний шлях: Галузь -> Спеціальність"""
        parts = [self.knowledge_field.name, self.name]
        if self.parent:
            parts.insert(1, self.parent.name)
        return " / ".join(parts)
