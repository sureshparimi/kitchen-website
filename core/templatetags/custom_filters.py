from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return float(value) * float(arg)

@register.filter
def get_range(value):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):
    {% for i in 5|get_range %}
        <span>{{ i }}</span>
    {% endfor %}
    """
    return range(int(value))
