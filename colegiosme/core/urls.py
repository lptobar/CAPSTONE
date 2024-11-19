from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('', home, name='inicio'),
    path('logout/', cerrar_sesion, name='logout'),

    ## -- ANOTACIONES -- ##
    path('anotaciones-asignaturas/', anotaciones_asignaturas, name='anotaciones-asignaturas'),
    path('anotaciones-estudiantes/<id>/', anotaciones_estudiantes, name='anotaciones-estudiantes'),
    path('portal-anotaciones/', portal_anotaciones, name='portal-anotaciones'),
    path('ver-anotaciones/<id>/', ver_anotaciones, name='ver-anotaciones'),
    path('crear-anotacion/<id>/', crear_anotacion, name='crear-anotacion'),

    ## -- NOTAS -- ##
    path('portal-notas-profesor/', portal_notas_profesor, name='portal-notas-profesor'),
    path('notas-asignatura/<id>/', notas_asignatura, name='notas-asignatura'),
    path('notas-curso/', notas_curso, name='notas-curso'),
    path('notas-curso/<id>/', notas_curso, name='notas-curso'),
    path('portal-notas-apoderado/', portal_notas_apoderado, name='portal-notas-apoderado'),
    path('notas-estudiante/<id>/', notas_estudiante, name='notas-estudiante'),

    ## -- ASISTENCIA -- ##
    path('portal-asistencia/', portal_asistencia, name='portal-asistencia'),
    path('asistencia-estudiante/<id>/', asistencia_estudiante, name='asistencia-estudiante'),
    path('asistencia-cursos/', asistencia_cursos, name='asistencia-cursos'),
    path('registrar-asistencia/<id>/', registrar_asistencia, name='registrar-asistencia'),
    path('ver-asistencia-admin/<id>/', ver_asistencia_admin, name='ver-asistencia-admin'),

    ## -- CURSOS -- ##
    path('listar-cursos/', listar_cursos, name='listar-cursos'),
    path('crear-curso/', crear_curso, name='crear-curso'),
    path('eliminar-curso/<id>/', eliminar_curso, name='eliminar-curso'),
    path('cerrar-curso/<id>/', cerrar_curso, name='cerrar-curso'),

    ## -- ASIGNATURAS -- ##
    path('listar-asignaturas/', listar_asignaturas, name='listar-asignaturas'),
    path('crear-asignatura/', crear_asignatura, name='crear-asignatura'),
    path('eliminar-asignatura/<id>/', eliminar_asignatura, name='eliminar-asignatura'),

    ## -- USUARIOS -- ##
    path('listar-usuarios/', listar_usuarios, name='listar-usuarios'),
    path('crear-usuario/', crear_usuario, name='crear-usuario'),
    path('editar-usuario/<id>/', editar_usuario, name='editar-usuario'),
    path('eliminar-usuario/<id>/', eliminar_usuario, name='eliminar-usuario'),

    ## -- MATRICULAS -- ##
    path('matricula-estudiante/', matricula_estudiante, name='matricula-estudiante'),
    path('matricula-padres/<id>/', matricula_padres, name='matricula-padres'),
    path('matricula-apoderado/<id>/', matricula_apoderado, name='matricula-apoderado'),
    path('crear-matricula/', crear_matricula, name='crear-matricula'),

    ## -- MENSUALIDADES -- ##
    path('listar-mensualidades/', listar_mensualidades, name='listar-mensualidades'),
    path('agregar-mensualidad/<id>/', agregar_mensualidad, name='agregar-mensualidades'),
    path('eliminar-mensualidad/<id>/', eliminar_mensualidad, name='eliminar-mensualidad'),
    path('restar-mensualidad/<id>/', restar_mensualidad, name='restar-mensualidad'),

    path('crear-noticia/', crear_noticia, name='crear-noticia'),
    path('listar-noticias/', listar_noticias, name='listar-noticias'),
    path('ver-noticia/<id>/', ver_noticia, name='ver-noticia'),
    path('editar-noticia/<id>/', editar_noticia, name='editar-noticia'),
    path('eliminar-noticia/<id>/', eliminar_noticia, name='eliminar-noticia'),

    ## -- INFORMES -- ##
    path('informe-notas-estudiante/<id>/', informe_notas_estudiante, name='informe-notas-estudiante'),
    path('informe-aprobados/<id>/', informe_aprobados, name='informe-aprobados'),

    ## -- WEBPAY -- ##
    path('webpay/', pago_webpay, name='webpay'),
    path('webpay-respuesta/', webpay_retorno, name='webpay-respuesta'),

    ## -- API HELPERS -- ##
    path('obtener_persona/<rut>/', obtener_persona),

    ## -- TAREA VISTA PROFESOR -- ##
    path('tareas/crear/', crear_tarea, name='crear_tarea'),
    path('tareas/', lista_tareas, name='lista_tareas'),
    path('tareas/entregas/<int:id_tarea>', ver_entrega_tarea, name='ver_entrega_tarea'),
    path('eliminar_tarea/<int:id_tarea>/', eliminar_tarea, name='eliminar_tarea'),
 
    ## -- TAREA VISTA ALUMNO -- ##
    path('tareas/alumno/', ver_tareas_alumno, name='tareas_alumno'),
    path('tareas/entregar/<int:id_tarea>', entregar_tarea , name='entregar_tarea'),
    path('obtener_asignaturas/<curso>/', obtener_asignaturas, name='obtener_asignaturas'),
    path('tareas/entregas/<id_tarea>/', ver_mis_entregas, name='ver_mis_entregas'),
    path('api/asignaturas/<curso>/', obtener_asignaturas2, name='api_asignaturas'),
    ## -- HORARIO -- ##
    path('crear_horario/<id_curso>', horario, name='horario'),
    path('eliminar_horario/<int:id_horario>', eliminar_horario, name='eliminar_horario'),
    path('asignar_asignatura/', asignar_asignatura, name='asignar_asignatura'),
    path('listar_horarios/', listar_horarios, name='listar_horarios'),
    path('horario_alumno/', horario_alumno, name='horario_alumno'),
    path('horario_alumno_ap/<int:id_persona>', horario_alumno_ap, name='horario_alumno_ap'),
    path('horario_apoderado/', horario_apoderado, name='horario_apoderado'),
    path('horario_profesor/', horario_profesor, name='horario_profesor'),

    ## -- BLOQUE HORARIO -- ##
    path('bloques_horarios/', listar_bloques_horarios, name='listar_bloques_horarios'),
    path('bloques_horarios/crear/', crear_bloque_horario, name='crear_bloque_horario'),
    path('bloques_horarios/actualizar/<int:bloque_id>/', actualizar_bloque_horario, name='actualizar_bloque_horario'),
    path('bloques_horarios/eliminar/<int:bloque_id>/', eliminar_bloque_horario, name='eliminar_bloque_horario'),

    ## -- MENSAJERIA INTERNA -- ##
    path('bandeja_entrada/', bandeja_entrada, name='bandeja_entrada'),
    path('detalle_mensaje/<int:id_mensaje>/', detalle_mensaje, name='detalle_mensaje'),
    path('nuevo_mensaje/', nuevo_mensaje, name='nuevo_mensaje'),
    path('api/destinatarios/', obtener_destinatarios, name='obtener_destinatarios'),
    path('responder_mensaje/<int:id_mensaje>/', responder_mensaje, name='responder_mensaje'),

    ## -- ENTREVISTAS -- ##
    path('ver-reuniones/', ver_reuniones, name='ver-reuniones'),
    path('info-reunion/<id>/', info_reunion, name='info-reunion'),
    path('agendar-reunion/<fecha>/', agendar_reunion, name='agendar-reunion'),
    path('obtener-reuniones/', obtener_reuniones)

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
