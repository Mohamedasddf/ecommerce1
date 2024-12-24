from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """
    Custom filter to multiply two numbers.
    Usage: {{ value|multiply:arg }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
