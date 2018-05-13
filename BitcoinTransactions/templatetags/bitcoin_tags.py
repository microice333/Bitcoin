from django import template

register = template.Library()


@register.filter
def satoshi_to_bitcoin(value):
    """
    Convert value from satoshi to bitcoin
    :param value: Value of transaction in Satoshi
    :return: Value of transaction in bitcoin
    """
    return value / 100000000