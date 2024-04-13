from django.contrib.auth.models import AbstractUser
from django.db import models

from publishings.models import Subscription

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    is_active = models.BooleanField(default=False, verbose_name='Активен')

    verification_token = models.CharField(max_length=20, **NULLABLE, verbose_name='Токен')
    phone = models.CharField(max_length=35, **NULLABLE, unique=True, verbose_name='Телефон')
    avatar = models.ImageField(**NULLABLE, upload_to='app_user/avatar', verbose_name='Аватар')
    country = models.CharField(**NULLABLE, max_length=150, verbose_name='страна')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    METHOD_CHOICES = [
        ('transfer', 'Перевод на счет'),
        ('cash', 'Наличные'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    pay_date = models.DateField(verbose_name='Дата оплаты')
    pay_subscribe = models.ForeignKey(Subscription, on_delete=models.CASCADE, verbose_name='Подписка оплачена',
                                      **NULLABLE)
    money = models.IntegerField(verbose_name='Оплаченная сумма')
    pay_method = models.CharField(choices=METHOD_CHOICES, default=METHOD_CHOICES[0],
                                  verbose_name='Способ оплаты')

    def __str__(self):
        return f'{self.money}'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплата'
