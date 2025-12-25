from django.db import models
from django.conf import settings

class Resume(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='resumes',
        verbose_name="Користувач"
    )
    title = models.CharField(max_length=255, verbose_name="Посада / Заголовок")
    description = models.TextField(verbose_name="Про себе / Досвід")
    is_active = models.BooleanField(default=True, verbose_name="Активне")
    is_anonymous = models.BooleanField(
        default=True, 
        verbose_name="Анонімний профіль",
        help_text="Якщо увімкнено, рекрутери бачитимуть лише ваш досвід без контактів"
    )
    expected_salary = models.PositiveIntegerField(null=True, blank=True, verbose_name="Очікувана зарплата (грн)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Резюме"
        verbose_name_plural = "Резюме"

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class ContactRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Очікує'
        APPROVED = 'APPROVED', 'Схвалено'
        REJECTED = 'REJECTED', 'Відхилено'

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='contact_requests')
    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_contact_requests'
    )
    message = models.TextField(blank=True, verbose_name="Повідомлення від рекрутера")
    status = models.CharField(
        max_length=10, 
        choices=Status.choices, 
        default=Status.PENDING,
        verbose_name="Статус"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Запит контактів"
        verbose_name_plural = "Запити контактів"
        unique_together = ('resume', 'recruiter')
