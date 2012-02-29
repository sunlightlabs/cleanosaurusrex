from django import template
register = template.Library()

@register.filter
# return the absolute value
def absvalue(value):
    try:
        return abs(value)
    except TypeError:
        return value
