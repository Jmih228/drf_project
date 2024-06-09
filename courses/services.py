from DRF.settings import STRIPE_API_KEY
import stripe


stripe.api_key = STRIPE_API_KEY


def creating_stripe_price(price):

    return stripe.Price.create(
        currency='rub',
        unit_amount=price * 100,
        product_data={'name': 'Payment'}
    )


def create_stripe_session(price):

    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
