from .models import EstadoMensaje, Contacto, RespuestaContacto
from django.db.models import Exists, OuterRef

def Mensaje_no_leidos(request):
    if request.user.is_authenticated:
        
        contador_mensajes_no_leidos = EstadoMensaje.objects.filter(destinatario=request.user, estado_leido=False).count()
        return {'mensaje_no_leidos': contador_mensajes_no_leidos}
    return {}

def contador_contactos_sin_respuesta(request):
    if request.user.is_authenticated:
        # Calcula el número de contactos sin respuesta
        contactos_sin_respuesta = Contacto.objects.annotate(
            tiene_respuesta=Exists(
                RespuestaContacto.objects.filter(contacto_id=OuterRef('id_contacto'))
            )
        ).filter(tiene_respuesta=False)
        return {'contador_sin_respuesta': contactos_sin_respuesta.count()}
    return {'contador_sin_respuesta': 0}