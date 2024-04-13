import stripe
import os

from config.settings import STRIPE_SECRET_API_KEY

API_KEY = STRIPE_SECRET_API_KEY


def get_session(id_profile, id_user):
    """ Функция возвращает сессию для оплаты """
    stripe.api_key = API_KEY

    product = stripe.Product.create(
        name=f'{id_profile}'
    )

    price = stripe.Price.create(
        currency='eur',
        unit_amount=100,
        product=f'{product.id}',
        metadata={"id_profile": id_profile, 'id_user': id_user}
    )

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[
            {
                'price': f'{price.id}',
                'quantity': 1,
            }
        ],
        mode='payment',
        metadata={"id_profile": id_profile, 'id_user': id_user}

    )

    return session.url
