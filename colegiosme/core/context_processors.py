from .models import EstadoMensaje

def Mensaje_no_leidos(request):
    if request.user.is_authenticated:
        
        contador_mensajes_no_leidos = EstadoMensaje.objects.filter(destinatario=request.user, estado_leido=False).count()
        return {'mensaje_no_leidos': contador_mensajes_no_leidos}
    return {}
