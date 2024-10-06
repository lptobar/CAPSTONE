from django import template
from django.apps import apps
from core.models import *
register = template.Library()

@register.filter
def getnumber(value):
    value = 7 - value
    number = ''.join(str(i) for i in range(1, value + 1))
    return number