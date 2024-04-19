import stripe
from config.settings import STRIPE_SECRET_API_KEY, WEB

# Устанавливаем секретный ключ Stripe API
API_KEY = STRIPE_SECRET_API_KEY


def get_session(id_profile, id_user):
    """ Функция создает сессию для оплаты и возвращает URL для перенаправления пользователя на оплату. """
    stripe.api_key = API_KEY

    # Создаем продукт в Stripe с именем, соответствующим идентификатору профиля
    product = stripe.Product.create(
        name=f'{id_profile}'
    )

    # Создаем цену для продукта с указанием валюты и стоимости в евро
    price = stripe.Price.create(
        currency='eur',
        unit_amount=100,  # Стоимость в центах (100 центов = 1 евро)
        product=f'{product.id}',  # Привязываем цену к созданному продукту
        metadata={"id_profile": id_profile, 'id_user': id_user}  # Добавляем метаданные для цены
    )

    # Создаем сессию оплаты с указанием успешного URL перенаправления и товарной позиции для оплаты
    session = stripe.checkout.Session.create(
        success_url=f"{WEB}",  # Указываем URL для перенаправления после успешной оплаты
        line_items=[
            {
                'price': f'{price.id}',  # Идентификатор цены для товарной позиции
                'quantity': 1,  # Количество товарных позиций
            }
        ],
        mode='payment',  # Указываем режим оплаты
        metadata={"id_profile": id_profile, 'id_user': id_user}  # Добавляем метаданные для сессии оплаты

    )

    return session.url  # Возвращаем URL для перенаправления пользователя на страницу оплаты
