from django.template import Library
from utils import utils

register = Library()

@register.filter
def price_format(value):
    return utils.price_format(value)

@register.filter
def cart_total_amount(cart):
    return utils.cart_total_amount(cart)

@register.filter
def cart_totals(cart):
    return utils.cart_totals(cart)