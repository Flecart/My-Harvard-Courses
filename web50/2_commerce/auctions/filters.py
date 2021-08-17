from django.template import Library

register = Library()

@register.filter
def usd(number):
    return f"{number}$"


@register.filter
def to_string(object):
    return str(object)


@register.filter
def filter_bidder(object):
    return str(object).split(" ")[0].replace("_", " ")