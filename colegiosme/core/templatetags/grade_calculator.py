from django import template
register = template.Library()

@register.filter
def average_grade(notas):
    try:
        return round(sum(notas) / len(notas), 1)
    except ZeroDivisionError:
        return 0.0