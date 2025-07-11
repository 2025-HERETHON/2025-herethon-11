from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(key, 0)

@register.filter
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

