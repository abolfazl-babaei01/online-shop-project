from django import template
from orders.models import Order

register = template.Library()


@register.filter
def three_digit_currency(value):
    return f'{int(value):,} تومان '


@register.simple_tag
def last_order(user):
    return Order.objects.filter(buyer_id=user.id)[:2]


@register.simple_tag
def multiply(total, price):
    return f'{total*price:,} تومان '
