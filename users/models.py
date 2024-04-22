from django.contrib.auth.models import AbstractUser
from django.db import models

from publishings.models import Subscription

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(**NULLABLE, verbose_name='Почта')
    is_active = models.BooleanField(default=False, verbose_name='Активен')

    verification_token = models.CharField(max_length=20, **NULLABLE, verbose_name='Токен')
    phone = models.CharField(max_length=35, unique=True, verbose_name='Телефон')
    avatar = models.ImageField(**NULLABLE, upload_to='app_user/avatar', verbose_name='Аватар')
    country = models.CharField(**NULLABLE, max_length=150, verbose_name='страна')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
