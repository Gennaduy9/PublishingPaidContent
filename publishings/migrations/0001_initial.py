# Generated by Django 5.0.3 on 2024-04-11 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=500, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=100, verbose_name="Фамилия")),
                (
                    "content",
                    models.TextField(
                        blank=True, null=True, verbose_name="Содержимое статьи"
                    ),
                ),
                ("email", models.EmailField(max_length=50, verbose_name="Почта")),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="profiles/",
                        verbose_name="Аватар",
                    ),
                ),
                (
                    "is_status",
                    models.BooleanField(default=False, verbose_name="Статус"),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now=True,
                        null=True,
                        verbose_name="Время и дата создание поста",
                    ),
                ),
                ("price", models.PositiveIntegerField(null=True, verbose_name="Цена")),
            ],
            options={
                "verbose_name": "Профиль",
                "verbose_name_plural": "Профили",
                "ordering": ("last_name",),
            },
        ),
        migrations.CreateModel(
            name="ProfilePayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "price_amount",
                    models.CharField(
                        blank=True, null=True, verbose_name="Цена платежа"
                    ),
                ),
                (
                    "payment_link",
                    models.URLField(
                        blank=True,
                        max_length=400,
                        null=True,
                        verbose_name="Ссылка на оплату",
                    ),
                ),
                (
                    "payment_id",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Идентификатор платежа",
                    ),
                ),
            ],
            options={
                "verbose_name": "Оплата",
                "verbose_name_plural": "Оплата",
            },
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Время и дата создание подписки"
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("created", "Подписан"), ("finished", "Отписался")],
                        default="created",
                        max_length=20,
                        verbose_name="Статус",
                    ),
                ),
            ],
            options={
                "verbose_name": "Подписка",
                "verbose_name_plural": "Подписки",
                "permissions": [
                    (
                        "Can_view_any_information_subscriptions.",
                        "Can view any subscriptions.",
                    ),
                    (
                        "They_cannot_edit_subscriptions.",
                        "They cannot edit subscriptions.",
                    ),
                    (
                        "Unable_to_manage_the_list_of_subscriptions.",
                        "Unable to manage the list of subscriptions.",
                    ),
                ],
            },
        ),
    ]
