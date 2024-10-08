from django.urls import path
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
     ## -- TAREA VISTA ALUMNO -- ##
    path('tareas/alumno/', ver_tareas_alumno, name='tareas_alumno'),
    path('tareas/entregar/<int:id_tarea>', entregar_tarea, name='entregar_tarea'),
]