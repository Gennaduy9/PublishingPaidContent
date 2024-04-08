from django.db import models

NULLABLE = {"blank": True, "null": True}


class Subscription(models.Model):
    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('finished', 'Завершена'),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время и дата создание подписки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name='Статус')
    stripe_customer_id = models.CharField(max_length=20, verbose_name='Идентификатор клиента')
    subscription_id = models.CharField(max_length=20, verbose_name='Идентификатор подписки')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return str(self.created_at)

    class Meta:
        permissions = [
            ("Can_view_any_information_subscriptions.", "Can view any subscriptions."),
            ("They_cannot_edit_subscriptions.", "They cannot edit subscriptions."),
            ("Unable_to_manage_the_list_of_subscriptions.", "Unable to manage the list of subscriptions."),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Profile(models.Model):
    first_name = models.CharField(max_length=500, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    content = models.TextField(**NULLABLE, verbose_name='Содержимое статьи')
    email = models.EmailField(max_length=50, unique=False, verbose_name='Почта')
    avatar = models.ImageField(upload_to='profiles/', **NULLABLE, verbose_name='Аватар')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачен')
    subscribe = models.ForeignKey(Subscription, on_delete=models.CASCADE, **NULLABLE, verbose_name='Подписаться')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.content}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ('last_name',)
