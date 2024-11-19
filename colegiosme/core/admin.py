from django.contrib import admin
from .models import Mensaje, EstadoMensaje, HistoriaMensaje

admin.site.register(Mensaje)
admin.site.register(EstadoMensaje)
admin.site.register(HistoriaMensaje)
# Register your models here.
