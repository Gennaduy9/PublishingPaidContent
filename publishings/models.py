from django.conf import settings
from django.db import models

NULLABLE = {"blank": True, "null": True}


class Profile(models.Model):
    first_name = models.CharField(max_length=500, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    content = models.TextField(**NULLABLE, verbose_name='Содержимое статьи')
    email = models.EmailField(max_length=50, unique=False, verbose_name='Почта')
    avatar = models.ImageField(upload_to='profiles/', **NULLABLE, verbose_name='Аватар')
    is_status = models.BooleanField(default=False, verbose_name='Статус')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', null=True)
    created = models.DateTimeField(auto_now=True, **NULLABLE, verbose_name='Время и дата создание поста')
    price = models.PositiveIntegerField(null=True, verbose_name='Цена')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.content}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ('last_name',)


# class ProfilePayment(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Название продукта', **NULLABLE)
#     price_amount = models.CharField(verbose_name='Цена платежа', **NULLABLE)
#     payment_link = models.URLField(max_length=400, verbose_name='Ссылка на оплату', **NULLABLE)
#     payment_id = models.CharField(max_length=255, verbose_name='Идентификатор платежа', **NULLABLE)
#
#     def __str__(self):
#         return self.payment_id
#
#     class Meta:
#         verbose_name = 'Оплата'
#         verbose_name_plural = 'Оплата'


class Subscription(models.Model):
    STATUS_CHOICES = (
        ('created', 'Подписан'),
        ('finished', 'Отписался'),
    )
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Время и дата создание подписки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Профиль')

    def __str__(self):
        #return str(self.created_at)
        return str(self.status)

    class Meta:
        permissions = [
            ("Can_view_any_information_subscriptions.", "Can view any subscriptions."),
            ("They_cannot_edit_subscriptions.", "They cannot edit subscriptions."),
            ("Unable_to_manage_the_list_of_subscriptions.", "Unable to manage the list of subscriptions."),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
