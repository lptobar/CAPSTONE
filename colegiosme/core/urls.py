from django.urls import path
from .views import *

urlpatterns = [
    ## INICIO ##
    path('', inicio, name='inicio'),

    ## MATRICULAS ##
    path('matricula-est/', matriculasEst, name='matriculasEst'),
    path('matricula-infoest/<id>', matriculasInfoest, name='matriculasInfoest'),
    path('matricula-pdr/<id>', matriculasPdr),
    path('matricula-apd/<id>', matriculasApd),
    path('matricula-ok/<id>', matriculaOk, name='matriculaOk'),

    ## NOTICIAS ##
    path('crear-noticia/', crearNoticia, name='crearNoticia'),
    path('listar-noticias/', listarNoticias, name='listarNoticias'),
    path('editar-noticia/<id>', editarNoticia, name='editarNoticia'),
    path('eliminar-noticia/<id>', eliminarNoticia, name="eliminarNoticia"),
    path('noticia/<id>', noticia, name='noticia'),

    ## LOGIN ##
    path('login/', iniciarSesion, name='login'),
    path('logout/', cerrarSesion, name='logout'),

    ## CURSOS ##
    path('listar-cursos/', listarCursos, name="listarCursos"),
    path('crear-curso/', crearCurso, name="crearCurso"),
    path('eliminar-curso/<id>', eliminarCurso, name="eliminarCurso"),
    path('cerrar-curso/<id>', cerrarCurso, name='cerrarCurso'),
    
    ## CURSOS REPROBADOS ##
    path('listar-cursos-reprobados/<id>', listarCursosReprobados, name="listarCursosReprobados"),
    path('crear-curso-reprobado/<id>', crearCursoReprobado, name="crearCursoReprobado"),
    path('editar-curso-reprobado/<id>', editarCursoReprobado, name="editarCursoReprobado"),
    path('eliminar-curso-reprobado/<id>', eliminarCursoReprobado, name="eliminarCursoReprobado"),

    ## MENSUALIDAD ##
    path('mensualidad/', listarMensualidad, name="listarMensualidad"),
    path('agregar/<int:id>', agregarMensualidad, name="AgregarMensualidad"),
    path('eliminar/<int:id>', eliminarMensualidad, name="EliminarMensualidad"),
    path('restar/<int:id>', restarMensualidad, name="RestarMensualidad"),
    path('webpay/', pagoWebpay, name="PagoWebpay"),
    path('webpay-respuesta/', webPayPlusRetorno, name="WebPayPlusRetorno"),
    
    ## ASISTENCIA ##
    path('asistencia-cursos/', asistenciaCursos, name="asistenciaCursos"),
    path('asistencia-estudiantes/<id>', asistenciaEstudiantes, name="asistenciaEstudiantes"),
    path('portal-asistencia/', portalAsistencia, name='portalAsistencia'),
    path('ver-asistencia-alumno/<id>', verAsistenciaAlumno, name='verAsistenciaAlumno'),
    path('ver-asistencia/<id>', verAsistencia, name='verAsistencia'),


    ## NOTAS ##
    path('notas-curso/', notasCurso, name="notasCurso"),
    path('notas-curso/<id>', notasCurso, name="notasCurso"),
    path('notas-asignatura/<id>', notasAsignatura, name="notasAsignatura"),
    path('notas-estudiante/<id>', notasEstudiante, name="notasEstudiante"),
    path('portal-notas-profesor/', portalNotasProfesor, name='portalNotasProfesor'),
    path('portal-notas-apoderado/', portalNotasApoderado, name='portalNotasApoderado'),

    ## ANOTACIONES ##
    path('anotaciones-asignaturas/', anotacionesAsignaturas, name="anotacionesAsignaturas"),
    path('anotaciones-estudiantes/<id>', anotacionesEstudiantes, name="anotacionesEstudiantes"),
    path('portal-anotaciones/', portalAnotaciones, name='portalAnotaciones'),
    path('anotaciones-estudiante/<id>', anotacionesEstudiante, name='anotacionesEstudiante'),
    path('crear-anotaciones/<id>', crearAnotacion, name="crearAnotacion"),

    ## GRUPO FAMILIAR ##
    path('listar-grupoFamiliar/<id>', listarGrupoFamiliar, name="listarGrupoFamiliar"),
    path('crear-grupoFamiliar/<id>', crearGrupoFamiliar, name="crearGrupoFamiliar"),
    path('editar-grupoFamiliar/<id>', editarGrupoFamiliar, name="editarGrupoFamiliar"),
    path('eliminar-grupoFamiliar/<id>', eliminarGrupoFamiliar, name="eliminarGrupoFamiliar"),

    ## ASIGNATURA ##
    path('listar-asignaturas/', listarAsignaturas, name='listarAsignaturas'),
    path('crear-asignatura/', crearAsignatura, name='crearAsignatura'),
    path('portal-asistencia/<id>', portalAsistencia, name='portalAsistencia'),
    path('eliminar-asignatura/<id>', eliminarAsignatura, name='eliminarAsignatura'),
    
    ## USUARIOS ##
    path('listar-usuarios/', listarUsuario, name='listarUsuarios'),
    path('crear-usuarios/', crearUsuario, name='crearUsuario'),
    path('editar-usuarios/', editarUsuario, name='editarUsuario'),
    path('eliminar-usuario/<id>', eliminarUsuario, name='eliminarUsuario'),
    path('crear-profesor/', crearProfesor, name='crearProfesor'),
    path('editar-profesor/<id>', editarProfesor, name='editarProfesor'),
    path('crear-administrador/', crearAdministrador, name='crearAdministrador'),
    path('editar-administrador/<id>', editarAdministrador, name='editarAdministrador'),

    ## INFORMES ##
    path('informe-matricula/<id>', informeMatricula, name='informeMatricula'),
    path('informe-notas-est/<id>', informeNotasEst, name='informeNotasEst'),
    path('informe-aprobados/<id>', informeAprobados, name='informeAprobados'),

    ####### API #######
    ## ALUMNO ##
    path('getPerson/<run>', getPerson),
    path('createMatriculaStudent/', createMatriculaStudent),
    path('getStudentInfo/<id>', getStudentInfo),
    path('updateStudentInfo/<id>', updateStudentInfo),

    ## PADRES ##
    path('getFatherInfo/<id>', getFatherInfo),
    path('createFather/<id>', createFather),

    ## APODERADOS ##
    path('createApoderado/<id>', createApoderado),

    ## PROFESOR ##
    path('createTeacher/', createTeacher),

    ## ADMINISTRADOR ##
    path('createAdmin/', createAdmin),
]