import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course):
    return stripe.Product.create(
        name=course.title,
        description=course.description,
    )


def create_stripe_price(product, amount):
    return stripe.Price.create(
        product=product.id,
        unit_amount=amount * 100,
        currency="rub",
    )


def create_stripe_session(price):
    return stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price": price.id, "quantity": 1}],
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
