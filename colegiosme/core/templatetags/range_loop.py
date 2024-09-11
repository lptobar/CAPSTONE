from django import template
from django.apps import apps
from core.models import *
register = template.Library()

@register.filter
def getnumber(value):
    value = 7 - value
    number = ''.join(str(i) for i in range(1, value + 1))
    return number

@register.filter
def getField(id, field):
    try:
        model = Responsable.objects.get(run=id)
        field_names = field.split('.')
        value = model

        for name in field_names:
            value = getattr(value, name)
        
        return value
    except (AttributeError, ValueError, LookupError, Responsable.DoesNotExist):
        return None
