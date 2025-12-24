from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Type(models.TextChoices):
        CANDIDATE = 'CANDIDATE', 'Шукач'
        RECRUITER = 'RECRUITER', 'Рекрутер'

    user_type = models.CharField(
        max_length=10,
        choices=Type.choices,
        default=Type.CANDIDATE,
        verbose_name="Тип користувача"
    )

    @property
    def is_candidate(self):
        return self.user_type == self.Type.CANDIDATE

    @property
    def is_recruiter(self):
        return self.user_type == self.Type.RECRUITER

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"


