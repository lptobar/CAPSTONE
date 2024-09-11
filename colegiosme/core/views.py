from django.shortcuts import render, redirect, get_object_or_404
from transbank.webpay.webpay_plus.transaction import Transaction
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from rest_framework.response import Response
from django.db.models import Max, Sum, Q
from django.contrib import messages
from django.http import QueryDict
from .serializers import *
from datetime import datetime, date
from .carro import Carro
from .models import *
from .forms import *
import random
import json
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse,JsonResponse

# Create your views here readonly.
def inicio(request):
    id_alta = 1
    noticias_prioridad_alta = Noticia.objects.filter(id_prioridad_noticia=id_alta)
    noticias = Noticia.objects.all()

    data= {
        'NoticiasAlta': noticias_prioridad_alta,
        'Noticias': noticias
    }
    return render(request, 'index.html', data)

## MATRICULAS ##
def matriculasEst(request):
    nacionalidades = Nacionalidad.objects.all()
    generos = Genero.objects.all()
    cursos = Curso.objects.filter(~Q(anio_curso=str(datetime.now().year - 1)))

    data = {
        'cursos': cursos,
        'nacionalidades': nacionalidades,
        'generos': generos
    }

    return render(request, 'matricula/matricula-est.html', data)

def matriculasInfoest(request, id):
    try:
        matricula = Matricula.objects.get(id_matricula=id)
        
        return render(request, 'matricula/matricula-infoest.html', { 'id_matricula': id })
    except Matricula.DoesNotExist:
        return redirect('inicio')

def matriculasPdr(request, id):
    try:
        matricula = Matricula.objects.get(id_matricula=id)
        generos = Genero.objects.all()
        nacionalidades = Nacionalidad.objects.all()
        niveles_academicos = NivelAcademico.objects.all()

        data = {
            'id_matricula': id,
            'generos': generos,
            'nacionalidades': nacionalidades,
            'niveles_academicos': niveles_academicos
        }
                
        return render(request, 'matricula/matricula-pdr.html', data)
    except Matricula.DoesNotExist:
        return redirect('inicio')

def matriculasApd(request, id):
    matricula = Matricula.objects.filter(id_matricula=id)
    parentescos = Parentesco.objects.all()
    nacionalidades = Nacionalidad.objects.all()
    niveles_academicos = NivelAcademico.objects.all()
    generos = Genero.objects.all()

    data = {
            'id_matricula': id,
            'generos': generos,
            'parentescos': parentescos,
            'nacionalidades': nacionalidades,
            'niveles_academicos': niveles_academicos
        }

    if not matricula.exists():
        return redirect(to='inicio')
    
    return render(request, 'matricula/matricula-apd.html', data)

## AUTH ##
def iniciarSesion(request):
    data = {
        'form': UsuarioForm()
    }

    if request.method == 'POST':
        id_usuario = request.POST['id_usuario']
        password = request.POST['password']
        user = authenticate(request, username=id_usuario, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos ....')
    return render(request, 'auth/login.html', data)

def cerrarSesion(request):
    logout(request)
    
    return redirect('inicio')

## CURSOS ##
def listarCursos(request):
    cursos = Curso.objects.filter(id_estado_curso=1)

    return render(request, 'curso/listar-cursos.html', { 'cursos': cursos })

def crearCurso(request):
    data = {
        'form': CursoForm()
    }
    
    if request.method == 'POST':
        post_data=request.POST.copy()
        formulario = CursoForm(data=request.POST)
        if formulario.is_valid:
            try:
                lcurso = ListaCurso.objects.get(id_curso=request.POST['id_lista_curso'])
                id_nuevoId = f"{lcurso.nombre_curso.replace(' ','')}{request.POST['anio_curso']}{request.POST['id_jornada']}{request.POST['id_tipo_curso']}"
                post_data['id_curso'] = id_nuevoId
                request.POST = QueryDict('',mutable=True)
                request.POST.update(post_data)
                formulario = CursoForm(data=request.POST)
                formulario.save()
                messages.success(request, 'El curso se creo correctamente id: ' + id_nuevoId)
            except ValueError as e:
                messages.error(request, 'Error al crear el curso el ID: ' + id_nuevoId + ' ya existe')
            except:
                messages.error(request, 'Error en la Información')
            return redirect(to="listarCursos")
        else:
            data["form"] = formulario

    return render(request, 'curso/crear-curso.html', data)

def eliminarCurso(request, id):
    curso = get_object_or_404(Curso, id_curso=id)
    curso.delete()
    messages.success(request, 'Curso eliminado Satifactoriamente id: '+ id)
    
    return redirect(to="listarCursos")

def cerrarCurso(request, id):
    curso = Curso.objects.get(id_curso=id)
    estado_matricula = EstadoMatricula.objects.get(id_estado_matricula=1)
    estado_curso = EstadoCurso.objects.get(id_estado_curso=2)
    matriculas = Matricula.objects.filter(id_curso_matricula=curso, id_estado_matricula=estado_matricula)

    for matricula in matriculas:
        matricula.id_estado_matricula = estado_matricula
        matricula.save()

    curso.id_estado_curso = estado_curso
    curso.save()

    return redirect(f'/informe-aprobados/{curso.id_curso}')

## GRUPO FAMILIAR ##
def listarGrupoFamiliar(request, id):
    matricula = Matricula.objects.get(id_matricula=id)
    grupoFamiliar = GrupoFamiliar.objects.filter(run_alumno=matricula.run_alumno.run.run)

    data = {
        'grupoFamiliar': grupoFamiliar,
        'id_matricula': id
    }

    return render(request, 'grupoFamiliar/listar-grupoFamiliar.html', data)

def crearGrupoFamiliar(request, id):
    matricula = Matricula.objects.get(id_matricula=id)
    alumno = Alumno.objects.get(run=matricula.run_alumno.run.run)
    data = {
        'form': GrupoFamiliarForm(initial={ 'run_alumno': alumno }),
        'id_matricula': id
    }

    if request.method == 'POST':
        formulario = GrupoFamiliarForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(to=f"/listar-grupoFamiliar/{id}")
        else:
            data["form"] = formulario

    return render(request, 'grupoFamiliar/crear-grupoFamiliar.html', data)

def editarGrupoFamiliar(request, id, id_matricula):
    grupofamiliar = get_object_or_404(GrupoFamiliar, id_gr_fam=id)
    data = {
        'form': GrupoFamiliarForm(instance=grupofamiliar)
    }

    if request.method == 'POST':
        formulario = GrupoFamiliarForm(data=request.POST,instance=grupofamiliar)
        if formulario.is_valid():
            formulario.save()
            return redirect(to=f"/listar-grupoFamiliar/{id_matricula}")
        data['form'] = formulario

    return render(request, 'grupoFamiliar/editar-grupoFamiliar.html', data)

def eliminarGrupoFamiliar(request, id, id_matricula):
    curso = get_object_or_404(GrupoFamiliar, id_gr_fam=id)
    curso.delete()
    return redirect(to=f"listarGrupoFamiliar/{id_matricula}")

## USUARIOS ##
def crearUsuario(request):
    return render(request, 'usuarios/crear-usuario.html')

def listarUsuario(request):
    profesores = Profesor.objects.all()
    administradores = Administrador.objects.all()
    data = {
        'profesores': profesores,
        'administradores': administradores
    }

    return render(request, 'usuarios/listar-usuario.html', data)

def editarUsuario(request):
    return render(request,'usuarios/editar-usuario.html')

def eliminarUsuario(request, id):
    usuario = Usuario.objects.get(id_usuario=id)
    usuario.delete()

    return redirect(to="listarUsuarios")

## USUARIO PROFESOR ##
def crearProfesor(request):
    nacionalidad = Nacionalidad.objects.all()
    genero = Genero.objects.all()

    grado_academico = GradoAcademico.objects.all()
    titulo = Titulo.objects.all()
    mencion = Mencion.objects.all()

    data={
        'Nacionalidad': nacionalidad,
        'Genero': genero,
        'GradoAcademico': grado_academico,
        'Titulo': titulo,
        'Mencion': mencion,
    }

    return render(request, 'usuarios/crear-profesor.html',data)

def editarProfesor(request, id):
    profesor = Profesor.objects.get(run = id)
    persona = Persona.objects.get(run = id)

    nacionalidad = Nacionalidad.objects.all()
    genero = Genero.objects.all()
    region = Region.objects.all()
    comuna = Comuna.objects.all()

    grado_academico = GradoAcademico.objects.all()
    titulo = Titulo.objects.all()
    mencion = Mencion.objects.all()

    data = {
        'Nacionalidad': nacionalidad,
        'GradoAcademico': grado_academico,
        'Titulo': titulo,
        'Mencion': mencion,
        'Genero': genero,
        'Region': region,
        'Comuna': comuna,
        'Profesor': profesor,
        'Persona': persona
    }
    return render(request, 'usuarios/editar-profesor.html', data)
    
## USUARIO ADMINISTRADOR ##
def crearAdministrador(request):
    nacionalidades = Nacionalidad.objects.all()
    generos = Genero.objects.all()
    grados_academicos = GradoAcademico.objects.all()
    titulos = Titulo.objects.all()
    menciones = Mencion.objects.all()
    cargos = Cargo.objects.all()

    data = {
        'nacionalidades': nacionalidades,
        'generos': generos,
        'grados_academicos': grados_academicos,
        'titulos': titulos,
        'menciones': menciones,
        'cargos': cargos,
    }

    return render(request, 'usuarios/crear-administrador.html', data)

def editarAdministrador(request, id):
    administrador = Administrador.objects.get(run = id)
    persona = Persona.objects.get(run = id)

    nacionalidad = Nacionalidad.objects.all()
    genero = Genero.objects.all()
    region = Region.objects.all()
    comuna = Comuna.objects.all()

    grado_academico = GradoAcademico.objects.all()
    titulo = Titulo.objects.all()
    mencion = Mencion.objects.all()
    tipo_administrador = Cargo.objects.all()

    data = {
        'Nacionalidad': nacionalidad,
        'GradoAcademico': grado_academico,
        'Titulo': titulo,
        'Mencion': mencion,
        'TipoAdministrador': tipo_administrador,
        'Genero': genero,
        'Region': region,
        'Comuna': comuna,
        'Administrador': administrador,
        'Persona': persona
    }
    return render(request, 'usuarios/editar-administrador.html', data)

## USUARIO INFORME ##
def informeUsuario(request, id):
    matricula = Matricula.objects.get(id_matricula=id)
    alumno = Alumno.objects.get(run=matricula.run_alumno)
    responsables = ResponsableAlumno.objects.filter(run_alumno=alumno)
    data = {
        'usuarios': []
    }

    for responsable in responsables:
        usuario = Usuario.objects.get(username=responsable.run_responsable.run.run)
        data['usuarios'].append({ 'usuario': usuario.username, 'password': usuario.password })

## ASIGNATURAS ##
def listarAsignaturas(request):
    cursos = Curso.objects.all()
    asignaturas = Asignatura.objects.all()

    data = {
        'Cursos': cursos,
        'Asignaturas': asignaturas
    }

    return render(request, 'asignaturas/listar-asignatura.html', data)

def crearAsignatura(request):
    data = {
        'form': AsignaturaForm(),
    }

    if request.method == 'POST':
        post_data=request.POST.copy()
        formulario = CursoForm(data=request.POST)

        if formulario.is_valid:
            try:
                id_nuevoId = f"{request.POST['id_curso']}{request.POST['id_lista_asignatura']}{request.POST['run_profesor']}"
                post_data['id_asignatura'] = id_nuevoId
                request.POST = QueryDict('',mutable=True)
                request.POST.update(post_data)
                formulario = AsignaturaForm(data=request.POST)
                formulario.save()
                messages.success(request, 'La asignatura se Creo correctamente id: ' + id_nuevoId)
            except ValueError as e:
                messages.error(request, 'Error al crear la asignatura el ID: ' + id_nuevoId + ' ya existe')
            return redirect(to="listarAsignaturas")
        else:
            data["form"] = formulario

    return render(request, 'asignaturas/crear-asignatura.html', data)

def eliminarAsignatura(request, id):
    asignatura = Asignatura.objects.get(id_asignatura=id)
    asignatura.delete()
    return redirect(to="listarAsignaturas")

## CURSOS REPETIDOS ##
def listarCursosReprobados(request, id):
    matricula = Matricula.objects.get(id_matricula=id)
    cursos = CursoRepetido.objects.filter(run_alumno=matricula.run_alumno.run.run)

    data = {
        'cursos': cursos,
        'id_matricula': id
    }

    return render(request, 'cursosReprobados/listar-curso-reprobado.html', data)

def crearCursoReprobado(request, id):
    matricula = Matricula.objects.get(id_matricula=id)
    alumno = Alumno.objects.get(run=matricula.run_alumno.run.run)

    data = {
        'form': CursoRepetidoForm(initial={ 'run_alumno':  alumno.run }),
        'id_matricula': id
    }

    if request.method == 'POST':
        formulario = CursoRepetidoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('listarCursosReprobados', id)
        else:
            data["form"] = formulario

    return render(request, 'cursosReprobados/crear-curso-reprobado.html', data)

def editarCursoReprobado(request, id):
    curso = get_object_or_404(CursoRepetido, id=id)
    data = {
        'form': CursoRepetidoForm(instance=curso)
    }

    if request.method == 'POST':
        formulario = CursoRepetidoForm(data=request.POST,instance=curso)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listarCursosRepetido")
        else:
            data['form'] = formulario

    return render(request, 'cursosReprobados/editar-curso-reprobado.html', data)

def eliminarCursoReprobado(request, id):
    curso = get_object_or_404(CursoRepetido, id_curso=id)
    curso.delete()
    return redirect(to="listarCursosRepetido")

## PAGO MENSUALIDAD ##
def listarMensualidad(request):
    user = request.user
    data = {
        'User': user
    }

    if user.id_tipo_usuario.id_tipo_usuario != 2:
        messages.error(request, 'Usuario no posee los atributos para acceder a esta página')
        return redirect(to='inicio')
    else:
        responsable = ResponsableAlumno.objects.filter(run_responsable=user.username)
        matricula = Matricula.objects.all()
        mensualidad = Mensualidades.objects.all()
        data = {
            'Responsable': responsable,
            'Matricula': matricula,
            'Mensualidad': mensualidad
        }
       
    return render(request, 'mensualidad/mensualidad.html', data)

##PAGO MENSUALIDAD - Carro##
def agregarMensualidad(request,id):
    carro = Carro(request)
    mensualidad = Mensualidades.objects.get(id_mensualidad=id)
    carro.Agregar(mensualidad)

    return redirect(to='listarMensualidad')

def eliminarMensualidad(request, id):
    carro=Carro(request)
    mensualidad=Mensualidades.objects.get(id_mensualidad=id)
    carro.Eliminar(mensualidad)
    return redirect(to='listarMensualidad')

def restarMensualidad(request, id):
    carro = Carro(request)
    mensualidad = Mensualidades.objects.get(id_mensualidad=id)
    carro.Quitar(mensualidad)

    return redirect(to='ListarMensualidad')

def pagoWebpay(request):
    amount=0
    if "carro" in request.session.keys():
        for key, value in request.session["carro"].items():
            amount += int(value["monto"])
    else:
        url_anterior = request.META.get('HTTP_REFERER')
        messages.error(request, 'No Ingreso ninguna mensualidad a pagar, el carro esta vacío')
        return redirect(url_anterior)
    if amount >= 1:
        buy_order = str(random.randrange(1000000, 99999999))
        session_token = request.session.session_key
        return_url = 'http://190.161.35.216:8000/webpay-respuesta/'
        create_request = {
            "buy_order":buy_order,
            "session_id":session_token,
            "amount":amount,
            "return_url":return_url
        }
        response = (Transaction()).create(buy_order,session_token,amount, return_url)

        return render(request, 'webpay/create.html', { 'request': create_request,'response': response })
    else:
        url_anterior = request.META.get('HTTP_REFERER')
        messages.error(request, 'No Ingreso ninguna mensualidad a pagar, el carro esta vacío')
        return redirect(url_anterior)

@csrf_exempt
@require_GET
def webPayPlusRetorno(request):
    token = request.GET.get("token_ws")
    transaction = Transaction()
    response = transaction.commit(token=token)

    if response['status'] == 'AUTHORIZED':
        for key, value in request.session["carro"].items():
            id_mensualidad = int(value["id_mensualidad"])
            mensualidad = Mensualidades.objects.get(id_mensualidad=id_mensualidad)
            estadoMensualidad = EstadoMensualidad.objects.get(id_estado_mensualidad=2)
            mensualidad.id_estado_mensualidad=estadoMensualidad
            mensualidad.save()

        request.session["carro"] = {}
        request.session.modified = True

    return render (request, 'webpay/commit.html', { 'token': token, 'response': response })

## ASISTENCIAS ##
def asistenciaCursos(request):
    cursos = Curso.objects.all()
    fecha_actual = date.today()
    fecha_actual = fecha_actual.strftime("%d-%m-%Y")
    data= {
        'Cursos': cursos,
        'Fecha': fecha_actual
    }
    return render(request, 'asistencia/cursos-asistencia.html', data)

def asistenciaEstudiantes(request, id):
    curso = Curso.objects.get(id_curso=id)
    matriculas = Matricula.objects.filter(id_curso_matricula=id)
    alumnos = Alumno.objects.all()

    fecha_actual = date.today()
    fecha_actual = fecha_actual.strftime("%d-%m-%Y")

    alumnos_asistencia = []

    run_alumnos = matriculas.values_list('run_alumno', flat=True)
    alumnos_asistencia = alumnos.filter(run__in=run_alumnos)

    data = {
        
        'Curso': curso,
        'Matriculas': matriculas,
        'Alumnos': alumnos_asistencia,
        'Fecha': fecha_actual
    }

    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                if key.startswith('asistencia_'):
                    alumno_id = key.replace('asistencia_', '')
                    asistencia = value

                    # Guardar los datos en la base de datos
                    asistencia_obj = AsistenciaCurso()
                    asistencia_obj.fecha_asistencia = date.today()
                    asistencia_obj.id_curso = curso
                    alumnos2 = Alumno.objects.get(run=alumno_id)
                    asistencia_obj.run_alumno = alumnos2
                    tipoAsistencia = TipoAsistencia.objects.get(id_tipo_asistencia=int(asistencia))
                    asistencia_obj.id_tipo_asistencia = tipoAsistencia

                    asistencia_obj.id_asistencia_curso = f"{asistencia_obj.run_alumno.run}{asistencia_obj.id_curso.id_curso}{str(asistencia_obj.fecha_asistencia).replace('-','')}"
                    asistencia_obj.save()
            except ValueError as e:
                continue

        messages.success(request, 'Registro de asistencias de alumno, curso: ' + id + ' guardada satifactoriamente...')
        return redirect(to="asistenciaCursos")
    
    return render(request, 'asistencia/estudiantes-asistencia.html', data)

def portalAsistencia(request):
    user = request.user
    Alumnos = ResponsableAlumno.objects.filter(run_responsable=user.username)
    data = {
        'Alumnos': Alumnos
    }
    return render(request,'asistencia/portal-asistencia.html',data)

def verAsistenciaAlumno(request, id):
    alumno = Persona.objects.get(run=id)
    dataTotal = {
        'Alumno': alumno,
        'Total_Asistencias': AsistenciaCurso.objects.filter(run_alumno=id).count(),
        'Total_Asistencia': AsistenciaCurso.objects.filter(run_alumno=id, id_tipo_asistencia=1).count(),
        'Total_Inasistencia': AsistenciaCurso.objects.filter(run_alumno=id,id_tipo_asistencia=2).count(),
        'Total_Justificado':AsistenciaCurso.objects.filter(run_alumno=id, id_tipo_asistencia=3).count()
    }
    datos = {'text': f'Asistencia del Alumno: {dataTotal["Alumno"].p_nombre} {dataTotal["Alumno"].s_nombre} {dataTotal["Alumno"].appaterno} {dataTotal["Alumno"].apmaterno}',
           'subtext': 'Asistencia total: ' + str(dataTotal['Total_Asistencias']),
           'data': [{'value': dataTotal['Total_Asistencia'], 'name': 'Presentes'},
                    {'value': dataTotal['Total_Inasistencia'], 'name': 'Ausentes'},
                    {'value': dataTotal['Total_Justificado'], 'name': 'Justificado'}
                   ]
            }
    

    datos_json=json.dumps(datos)
    context={
        'datos_json':datos_json, 
    }
    return render(request,'asistencia/ver-asistencia-alumno.html',context)

def verAsistencia(request, id):
    curso = Curso.objects.get(id_curso=id)
    dataTotal = {
        'Curso': curso,
        'Total_Asistencias': AsistenciaCurso.objects.filter(id_curso=id).count(),
        'Total_Asistencia': AsistenciaCurso.objects.filter(id_curso=id, id_tipo_asistencia=1).count(),
        'Total_Inasistencia': AsistenciaCurso.objects.filter(id_curso=id,id_tipo_asistencia=2).count() + AsistenciaCurso.objects.filter(id_curso=id, id_tipo_asistencia=3).count()
    }
    datos = {'text': 'Asistencia del Curso : ' + dataTotal['Curso'].id_lista_curso.nombre_curso,
           'subtext': 'Asistencia total :' + str(dataTotal['Total_Asistencias']),
           'data': [{'value': dataTotal['Total_Asistencia'], 'name': 'Presentes'},
                    {'value': dataTotal['Total_Inasistencia'], 'name': 'Ausentes'}
                   ]
            }
    array_alumnos=[]

    array_asistencia=[]
    array_inasistencia = []
    array_justificado = []
    matriculas=Matricula.objects.filter(id_curso_matricula=id)
    for matricula in matriculas:

        persona=Persona.objects.get(run=matricula.run_alumno.run)
        nombre= persona.p_nombre+" "+persona.s_nombre + " "+ persona.appaterno + " "+persona.apmaterno
        array_alumnos.append(nombre)
        presente=AsistenciaCurso.objects.filter(run_alumno=persona.run, id_tipo_asistencia=1).count()
        ausente=AsistenciaCurso.objects.filter(run_alumno=persona.run, id_tipo_asistencia=2).count()
        justificado=AsistenciaCurso.objects.filter(run_alumno=persona.run, id_tipo_asistencia=3).count()
        array_asistencia.append(presente)
        array_inasistencia.append(ausente)
        array_justificado.append(justificado)

    array_serie = [
        {
            'name': 'Presente',
            'type': 'bar',
            'stack': 'total',
            'label': {
                'show': 'true'
            },
            'emphasis': {
                'focus': 'series'
            },
            'data': array_asistencia
        },
        {
            'name': 'Ausente',
            'type': 'bar',
            'stack': 'total',
            'label': {
                'show': 'true'
            },
            'emphasis': {
                'focus': 'series'
            },
            'data': array_inasistencia
        },
        {
            'name': 'Justificado',
            'type': 'bar',
            'stack': 'total',
            'label': {
                'show': 'true'
            },
            'emphasis': {
                'focus': 'series'
            },
            'data': array_justificado
        },
    ]
    datos_json3=json.dumps(array_alumnos)
    datos_json2=json.dumps(array_serie)
    datos_json=json.dumps(datos)
    context={
        'datos_json':datos_json,
        'datos_json2':datos_json2,
        'datos_json3': datos_json3
    }
    return render(request,'asistencia/ver-asistencia-admin.html',context)

## NOTAS ##
def notasCurso(request, id=None):
    cursos = Curso.objects.filter(anio_curso=str(datetime.now().year))
    data = {
        'cursos': cursos,
        'asignaturas': []
    }

    if id is not None:
        asignaturas = Asignatura.objects.filter(id_curso=id)

        for asignatura in asignaturas:
            notas = Notas.objects.filter(id_asignatura=asignatura).values_list('nota', flat=True)
            promedio = 0.0 if len(notas) == 0 else round(sum(notas) / len(notas), 1)
            data['asignaturas'].append({ 'asignatura': asignatura, 'promedio': promedio })

        return render(request, 'notas/notas-curso.html', data)
    else:
        asignaturas = Asignatura.objects.all()

        for asignatura in asignaturas:
            notas = Notas.objects.filter(id_asignatura=asignatura).values_list('nota', flat=True)
            promedio = 0.0 if len(notas) == 0 else round(sum(notas) / len(notas), 1)
            data['asignaturas'].append({ 'asignatura': asignatura, 'promedio': promedio })

        return render(request, 'notas/notas-curso.html', data)

def notasAsignatura(request, id):
    asignatura = Asignatura.objects.get(id_asignatura=id)
    curso = Curso.objects.get(id_curso=asignatura.id_curso.id_curso)
    matriculas = Matricula.objects.filter(id_curso_matricula=curso.id_curso, id_estado_matricula=1)
    notas_max_id = Notas.objects.order_by('-id_nota').first()
    notas_max_id = notas_max_id.id_nota if notas_max_id is not None else 0

    data = {
        'alumnos': []
    }
    
    for matricula in matriculas:
        alumno = Alumno.objects.get(run=matricula.run_alumno)
        notas = Notas.objects.filter(run_alumno=alumno, id_asignatura=asignatura)
        notas_max_id += 1

        data['alumnos'].append({ 'alumno': alumno, 'notas': notas, 'nota_max_id': notas_max_id })
    
    if request.method == 'POST':
        for name, value in request.POST.items():
            if name == 'csrfmiddlewaretoken' or value == '0': continue
            run, id_nota = name.split('nota')

            alumno = Alumno.objects.get(run=run)
            Notas.objects.update_or_create(
                id_nota = id_nota,
                defaults = {
                    'nota': float(value.replace(',', '.')),
                    'id_asignatura': asignatura,
                    'run_alumno': alumno
                }
            )
        messages.success(request, 'Notas guardadas con exito.')
        return redirect('portalNotasProfesor')
                        
    return render(request, 'notas/notas-asignatura.html', data)

def notasEstudiante(request, id):
    matricula = Matricula.objects.get(run_alumno=id, id_estado_matricula=1)
    asignaturas = Asignatura.objects.filter(id_curso=matricula.id_curso_matricula)
    data = {
        'alumno': matricula.run_alumno,
        'asignaturas': [],
        'promedio_total': 0
    }

    for asignatura in asignaturas:
        notas = Notas.objects.filter(run_alumno=matricula.run_alumno, id_asignatura=asignatura).values_list('nota', flat=True)
        promedio = 0.0 if len(notas) == 0 else round(sum(notas) / len(notas), 1)
        data['asignaturas'].append({ 'asignatura': asignatura, 'notas': notas, 'promedio': promedio })

    promedios = [d['promedio'] for d in data['asignaturas'] if d['promedio'] != 0.0]
    data['promedio_total'] = 0.0 if len(promedios) == 0 else round(sum(promedios) / len(promedios), 1)

    return render(request, 'notas/notas-estudiante.html', data)

def portalNotasProfesor(request):
    if not request.user.is_authenticated or request.user.id_tipo_usuario.id_tipo_usuario != 3:
        return redirect('inicio')
    else:
        user = request.user
        asignaturas = Asignatura.objects.filter(run_profesor=user.username, id_curso__anio_curso=str(datetime.now().year))

        data = {
            'asignaturas': []
        }
        for asignatura in asignaturas:
            notas = Notas.objects.filter(id_asignatura=asignatura.id_asignatura).values_list('nota', flat=True)
            data['asignaturas'].append({ 'info_asignatura': asignatura, 'notas': list(notas) })

        return render(request, 'notas/portal-notas-profesor.html', data)

def portalNotasApoderado(request):
    try:
        user = request.user
        responsables = ResponsableAlumno.objects.filter(run_responsable=user.username)

        data = {
            'alumnos': []
        }
        for responsable in responsables:
            alumno = Alumno.objects.get(run=responsable.run_alumno)
            data['alumnos'].append(alumno)

        return render(request, 'notas/portal-notas-apoderado.html', data)
    except Exception as e:
        return redirect('inicio')

## ANOTACIONES ##
def anotacionesAsignaturas(request):
    if not request.user.is_authenticated or request.user.id_tipo_usuario.id_tipo_usuario != 3:
        return redirect('inicio')
    
    user = request.user
    asignaturas = Asignatura.objects.filter(run_profesor=user.username)

    data = {
        'asignaturas': asignaturas
    }

    return render(request, 'anotaciones/anotaciones-asignaturas.html', data)

def anotacionesEstudiantes(request, id):
    tipo_anotaciones = TipoAnotacion.objects.all()
    asignatura = Asignatura.objects.get(id_asignatura=id)
    matriculas = Matricula.objects.filter(id_curso_matricula=asignatura.id_curso)
    
    data = {
        
        'tipo_anotaciones': tipo_anotaciones,
        'asignatura': asignatura,
        'alumnos': []
    }
    for matricula in matriculas:
        alumno = Alumno.objects.get(run=matricula.run_alumno)
        anotaciones = Anotacion.objects.filter(run_alumno=alumno, id_asignatura=asignatura)
        data['alumnos'].append({ 'alumno': alumno, 'anotaciones': anotaciones })

    return render(request, 'anotaciones/anotaciones-estudiantes.html', data)

def portalAnotaciones(request):
    if not request.user.is_authenticated:
        return redirect('inicio')
    
    user = request.user
    responsables = ResponsableAlumno.objects.filter(run_responsable=user.username)
    alumnos = Alumno.objects.filter(run__in=responsables.values('run_alumno'))

    data = {
        'alumnos': list(alumnos)
    }

    return render(request, 'anotaciones/portal-anotaciones.html', data)

def anotacionesEstudiante(request, id):
    matricula = Matricula.objects.get(run_alumno=id, id_estado_matricula=1)
    asignaturas = Asignatura.objects.filter(id_curso=matricula.id_curso_matricula)
    tipo_anotaciones = TipoAnotacion.objects.all()

    data = {
        'alumno': matricula.run_alumno,
        'tipo_anotaciones': tipo_anotaciones,
        'anotaciones': []
    }

    for asignatura in asignaturas:
        anotaciones = Anotacion.objects.filter(id_asignatura=asignatura, run_alumno=id)
        data['anotaciones'].append({ 'asignatura': asignatura, 'anotaciones': anotaciones })
    
    return render(request, 'anotaciones/anotaciones-estudiante.html', data)

def crearAnotacion(request, id):
    url_anterior = request.META.get('HTTP_REFERER')
    matricula = Matricula.objects.get(run_alumno=id, id_estado_matricula=1)
    curso = Curso.objects.get(id_curso=matricula.id_curso_matricula.id_curso)
    alumno = Alumno.objects.get(run=matricula.run_alumno)
    persona = Persona.objects.get(run=alumno.run)

    id_curso_alumno = curso.id_curso

    formulario = AnotacionForm(id=id, id_curso=id_curso_alumno)

    fecha_anotacion = date.today()

    if request.method == 'POST':
        formulario = AnotacionForm(request.POST, id=id)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'La anotación se creó correctamente')
            return redirect(url_anterior)
        else:
            messages.error(request, 'Error al crear la anotación')
    data = {
        'Curso': curso,
        'form': formulario,
        'Fecha': fecha_anotacion,
        'Alumno': persona
    }
    return render(request, 'anotaciones/crear-anotaciones.html', data)

## NOTICIAS ##
def listarNoticias(request):
    noticias = Noticia.objects.all()
    data= {
        'Noticias': noticias
    }
    return render(request, 'noticias/listar-noticia.html', data)

def crearNoticia(request):
    fecha_noticia = date.today()

    data = {
        'Fecha': fecha_noticia,
        'form': NoticiaForm
    }

    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'La noticia se creó correctamente')
            return redirect('listarNoticias')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo {field}: {error}')

    return render(request, 'noticias/crear-noticia.html',data)

def noticia(request, id):
    noticia = Noticia.objects.get(id_noticia=id)
    noticias = Noticia.objects.all()

    data={
        'Noticia': noticia,
        'Noticias': noticias
    }
    return render(request, 'noticias/noticia.html', data)

def editarNoticia(request, id):
    noticia = Noticia.objects.get(id_noticia=id)
    data = {
        'form': NoticiaForm(instance=noticia)
    }

    if request.method == 'POST':
        formulario = NoticiaForm(data=request.POST,instance=noticia)
        if formulario.is_valid():
            formulario.save()
            return redirect('listarNoticias')
        data['form'] = formulario

    return render(request, 'noticias/editar-noticia.html', data)

def eliminarNoticia(request, id):
    noticia = Noticia.objects.get(id_noticia=id)
    noticia.delete()
    messages.success(request, 'Noticia eliminada satifactoriamente')
    
    return redirect(to="listarNoticias")

## INFORMES ##
def matriculaOk(request, id):
    matricula = Matricula.objects.get(id_matricula=id)
    curso = Curso.objects.get(id_curso=matricula.id_curso_matricula.id_curso)
    alumno = Alumno.objects.get(run=matricula.run_alumno)
    persona = Persona.objects.get(run=alumno.run)

    data = {
        'matricula': matricula,
        'curso': curso,
        'alumno': alumno,
        'persona': persona
    }

    return render(request, 'matricula/matricula-ok.html', data)

def informeMatricula(request, id):
    # Obtiene la plantilla HTML que se utilizará para generar el PDF
    template = get_template('informes/informe-matricula.html')

    # Renderiza la plantilla con los datos necesario
    matricula = Matricula.objects.get(id_matricula=id)
    curso = Curso.objects.get(id_curso=matricula.id_curso_matricula.id_curso)
    alumno = Alumno.objects.get(run=matricula.run_alumno)
    persona = Persona.objects.get(run=alumno.run)
    responsables = ResponsableAlumno.objects.filter(run_alumno=matricula.run_alumno)

    data = {
        'matricula': matricula,
        'curso': curso,
        'persona': persona,
        'alumno': alumno,
        'responsables': responsables
    }

    html = template.render(data)

    # Crea el objeto HttpResponse con el tipo de contenido "application/pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Matricula{id}.pdf"'

    # Crea el objeto PDF utilizando el contenido HTML renderizado
    pisa.CreatePDF(html, dest=response)

    return response

def informeNotasEst(request, id):
    # Obtiene la plantilla HTML que se utilizará para generar el PDF
    template = get_template('informes/informe-notas-est.html')

    # Renderiza la plantilla con los datos necesario
    estado_matricula = EstadoMatricula.objects.get(id_estado_matricula=1)
    matricula = Matricula.objects.get(run_alumno=id, id_estado_matricula=estado_matricula)
    curso = Curso.objects.get(id_curso=matricula.id_curso_matricula.id_curso)
    asignaturas = Asignatura.objects.filter(id_curso=matricula.id_curso_matricula)
    data = {
        'alumno': matricula.run_alumno,
        'curso': curso,
        'asignaturas': [],
        'promedio_total': 0
    }

    for asignatura in asignaturas:
        notas = Notas.objects.filter(run_alumno=matricula.run_alumno, id_asignatura=asignatura).values_list('nota', flat=True)
        promedio = 0.0 if len(notas) == 0 else round(sum(notas) / len(notas), 1)
        data['asignaturas'].append({ 'asignatura': asignatura, 'notas': notas, 'promedio': promedio })

    promedios = [d['promedio'] for d in data['asignaturas'] if d['promedio'] != 0.0]
    data['promedio_total'] = round(sum(promedios) / len(promedios), 1)
        
    html = template.render(data)

    # Crea el objeto HttpResponse con el tipo de contenido "application/pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="documento.pdf"'

    # Crea el objeto PDF utilizando el contenido HTML renderizado
    pisa.CreatePDF(html, dest=response)

    return response

def informeAprobados(request, id):

    template = get_template('informes/informe-aprobados.html')

    curso = Curso.objects.get(id_curso=id)
    matriculas = Matricula.objects.filter(id_curso_matricula=curso)
    data = {
        'curso': curso,
        'alumnos': []
    }

    for matricula in matriculas:
        alumno = Alumno.objects.get(run=matricula.run_alumno)
        asignaturas = Asignatura.objects.filter(id_curso=matricula.id_curso_matricula)
        notas = Notas.objects.filter(run_alumno=matricula.run_alumno).values_list('nota', flat=True)
        promedio_final = 0.0 if len(notas) == 0 else round(sum(notas) / len(notas), 1)

        contador = 0
        for asignatura in asignaturas:
            notas = Notas.objects.filter(run_alumno=matricula.run_alumno, id_asignatura=asignatura.id_asignatura).values_list('nota', flat=True)
            promedio = 0.0 if len(notas) == 0 else round(sum(notas) / len(notas), 1)
            if promedio < 4.0:
                contador += 1

        estado = 'Reprobado' if contador > 2 and promedio_final < 5.0 else 'Aprobado'

        # notas = Notas.objects.filter(run_alumno=alumno).values_list('nota', flat=True)

        data['alumnos'].append({ 'alumno': alumno, 'promedio_final': promedio_final, 'estado': estado })

    html = template.render(data)

    # Crea el objeto HttpResponse con el tipo de contenido "application/pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="documento.pdf"'

    # Crea el objeto PDF utilizando el contenido HTML renderizado
    pisa.CreatePDF(html, dest=response)

    return response

## MATRICULAS (ESTUDIANTE)
@csrf_exempt
@api_view(['GET'])
def getPerson(request, run):
    try:
        persona = Persona.objects.get(run=run)
        alumno = Alumno.objects.filter(run=persona.run)
        responsable = Responsable.objects.filter(run=persona.run)
        profesor = Profesor.objects.filter(run=persona.run)
        administrador = Administrador.objects.filter(run=persona.run)
        data = model_to_dict(persona)

        direccion = Direccion.objects.get(id_direccion=data['id_direccion'])
        comuna = Comuna.objects.get(id_comuna=direccion.id_comuna.id_comuna)
        region = Region.objects.get(id_region=comuna.id_region.id_region)

        data['genero'] = data.pop('id_genero')
        data['nacionalidad'] = data.pop('id_nacionalidad')
        data['nombres'] = f'{data["p_nombre"]} {data["s_nombre"]}'
        data['nombre_calle'] = direccion.nombre_calle
        data['numero'] = direccion.numero
        data['region'] = region.nombre_region
        data['comuna'] = comuna.id_comuna
        data = data.copy()

        if alumno.exists():
            alumno = model_to_dict(alumno[0])
            data.update(alumno)
        if responsable.exists():
            responsable = model_to_dict(responsable[0])
            responsable['nivel_academico'] = responsable.pop('id_nivel_academico')
            responsable['parentesco'] = responsable.pop('id_parentesco')
            data.update(responsable)
        if profesor.exists():
            profesor = model_to_dict(profesor[0])
            data.update(profesor)
        if administrador.exists():
            administrador = model_to_dict(administrador[0])
            data.update(administrador)

        del data['p_nombre']
        del data['s_nombre']
        del data['id_direccion']

        return Response({ 'ok': True, 'data': data })
    except Exception as e:
        return Response({ 'ok': False, 'msg': str(e) })

@csrf_exempt
@api_view(['POST'])
def createMatriculaStudent(request):
    try:
        body = json.loads(json.dumps(request.data))
        comuna = Comuna.objects.get(id_comuna=body['comuna'])
        nacionalidad = Nacionalidad.objects.get(id_nacionalidad=body['nacionalidad'])
        genero = Genero.objects.get(id_genero=body['genero'])
        estado_alumno = EstadoAlumno.objects.get(id_estado_alumno=1)
        curso = Curso.objects.get(id_curso=body['curso_matricula'])
        estado_matricula = EstadoMatricula.objects.get(id_estado_matricula=1)

        if curso.matriculas_disponibles == 0:
            return Response({ 'ok': False, 'msg': 'El curso no tiene cupos disponibles' })

        direccion, _ = Direccion.objects.get_or_create(
            nombre_calle = body['nombre_calle'],
            numero = body['numero'],
            id_comuna = comuna
        )
        persona, _ = Persona.objects.update_or_create(
            run = body['rut'],
            defaults = {
                'p_nombre': body['p_nombre'],
                's_nombre': body['s_nombre'],
                'appaterno': body['appaterno'],
                'apmaterno': body['apmaterno'],
                'fecha_nacimiento': body['fecha_nacimiento'],
                'id_nacionalidad': nacionalidad,
                'telefono_fijo': body['telefono_fijo'],
                'celular': body['celular'],
                'email': body['email'],
                'id_direccion': direccion,
                'id_genero': genero
            }
        )
        alumno, _ = Alumno.objects.update_or_create(
            run = persona,
            defaults = {
                'id_estado_alumno': estado_alumno,
            }
        )
        matricula, created = Matricula.objects.get_or_create(
            id_matricula = f'{body["curso_matricula"]}{body["rut"]}',
            defaults = {
                'run_alumno': alumno,
                'id_curso_matricula': curso,
                'id_estado_matricula': estado_matricula
            }
        )

        if created:
            curso.matriculas_disponibles -= 1
            curso.save()

            return Response({ 'ok': True, 'id_matricula': matricula.id_matricula })
        else:
            return Response({ 'ok': False, 'msg': 'Este alumno ya estuvo matriculado a este curso' })
    except Exception as e:
        print(str(e))
        return Response({ 'ok': False, 'msg': str(e) })
    
### MATRICULAS (INFO ESTUDIANTE) ###
@csrf_exempt
@api_view(['GET'])
def getStudentInfo(request, id):
    try:
        matricula = Matricula.objects.get(id_matricula=id)
        alumno = Alumno.objects.get(run=matricula.run_alumno.run.run)
        data = model_to_dict(alumno)
        
        data['pertenece_etnia'] = False

        del data['run']
        del data['rut_padre']
        del data['rut_madre']
        del data['id_estado_alumno'],
        del data['seguro_escolar_particular']
        del data['discapacidad_fisica']

        return Response(data)
    except Exception as e:
        return Response({ 'ok': False, 'msg': str(e) })

@csrf_exempt
@api_view(['PUT'])
def updateStudentInfo(request, id):
    try:
        body = json.loads(json.dumps(request.data))
        matricula = Matricula.objects.get(id_matricula=id)
        alumno = Alumno.objects.get(run=matricula.run_alumno.run.run)

        alumno.colegio_procedencia = body['colegio_procedencia']
        alumno.razon_cambio_colegio = body['razon_cambio_colegio']
        alumno.estudiante_prioritario = body['estudiante_prioritario']
        alumno.evaluacion_profesional = body['evaluacion_profesional']
        alumno.enfermedad_cronica = body['enfermedad_cronica']
        alumno.medio = body['medio']
        alumno.pie = body['pie']

        if body['pertenece_etnia'] == 'true':
            alumno.etnia = body['etnia']

        alumno.save()

        return Response({ 'ok': True })
    except Exception as e:
        return Response({ 'ok': False, 'msg': str(e) })

## MATRICULAS (PADRES)
@csrf_exempt
@api_view(['GET'])
def getFatherInfo(request, id):
    try:
        matricula = Matricula.objects.get(id_matricula=id)
        alumno = Alumno.objects.get(run=matricula.run_alumno.run.run)

        padre = model_to_dict(Persona.objects.get(run=alumno.rut_padre.run))
        madre = model_to_dict(Persona.objects.get(run=alumno.rut_madre.run))
        responsable_padre = model_to_dict(Responsable.objects.get(run=padre['run']))
        responsable_madre = model_to_dict(Responsable.objects.get(run=madre['run']))

        ## Format data (padre)
        padre['rut'] = padre['run']
        padre['nombres'] = f'{padre["p_nombre"]} {padre["s_nombre"]}'
        padre['genero'] = padre.pop('id_genero')
        padre['vive_con_alumno'] = responsable_padre['vive_con_alumno']
        padre['nivel_academico'] = responsable_padre['id_nivel_academico']

        ## Format data (madre)
        madre['rut'] = madre['run']
        madre['nombres'] = f'{madre["p_nombre"]} {madre["s_nombre"]}'
        madre['genero'] = madre.pop('id_genero')
        madre['vive_con_alumno'] = responsable_madre['vive_con_alumno']
        madre['nivel_academico'] = responsable_madre['id_nivel_academico']

        ## Clean data
        del padre['run']
        del madre['run']
        del padre['p_nombre']
        del padre['s_nombre']
        del madre['p_nombre']
        del madre['s_nombre']
        

        data = {
            'padre': padre,
            'madre': madre
        }

        return Response({ 'ok': True, 'data': data })
    except Exception as e:
        return Response({ 'ok': False, 'msg': str(e) })

@csrf_exempt
@api_view(['POST'])
def createFather(request, id):
    try:
        body = json.loads(json.dumps(request.data))
        matricula = Matricula.objects.get(id_matricula=id)
        alumno_persona = Persona.objects.get(run=matricula.run_alumno.run.run)
        alumno = Alumno.objects.get(run=alumno_persona.run)

        for item in body.items():
            data = item[1]        
            genero = Genero.objects.get(id_genero=data['genero'])
            nacionalidad = Nacionalidad.objects.get(id_nacionalidad=data['nacionalidad'])
            parentesco = Parentesco.objects.get(nombre_parentesco=item[0].capitalize())
            nivel_academico = NivelAcademico.objects.get(id_nivel_academico=data['nivel_academico'])

            if data['vive_con_alumno']:
                direccion = Direccion.objects.get(id_direccion=alumno_persona.id_direccion.id_direccion)
                data['telefono_fijo'] = alumno.run.telefono_fijo
            else:
                comuna = Comuna.objects.get(id_comuna=data['comuna'])
                direccion, _ = Direccion.objects.get_or_create(
                    nombre_calle = data['nombre_calle'],
                    numero = data['numero'],
                    id_comuna = comuna
                )

            persona, _ = Persona.objects.update_or_create(
                run = data['rut'],
                defaults={
                    'p_nombre': data['p_nombre'],
                    's_nombre': data['s_nombre'],
                    'appaterno': data['appaterno'],
                    'apmaterno': data['apmaterno'],
                    'fecha_nacimiento': data['fecha_nacimiento'],
                    'id_nacionalidad': nacionalidad,
                    'telefono_fijo': data['telefono_fijo'],
                    'celular': data['celular'],
                    'email': data['email'],
                    'id_direccion': direccion,
                    'id_genero': genero
                }
            )
            
            responsable, _ = Responsable.objects.update_or_create(
                run = persona,
                defaults = {
                    'id_nivel_academico': nivel_academico,
                    'vive_con_alumno': data['vive_con_alumno'],
                    'id_parentesco': parentesco
                }
            )

        padre = Persona.objects.get(run=body['padre']['rut'])
        madre = Persona.objects.get(run=body['madre']['rut'])
        alumno = Alumno.objects.get(run=alumno_persona.run)

        alumno.rut_padre = padre
        alumno.rut_madre = madre
        alumno.save()

        return Response({ 'ok': True })
    except Exception as e:
        return Response({ 'ok': False, 'msg': str(e) })

## MATRICULAS (APODERADOS)
@csrf_exempt
@api_view(['POST'])
def createApoderado(request, id):
    try:
        body = json.loads(json.dumps(request.data))
        matricula = Matricula.objects.get(id_matricula=id)
        alumno_persona = Persona.objects.get(run=matricula.run_alumno.run.run)
        alumno_alumno = Alumno.objects.get(run=alumno_persona.run)

        for item in body.items():
            data = item[1]
            genero = Genero.objects.get(id_genero=data['genero'])
            nacionalidad = Nacionalidad.objects.get(id_nacionalidad=data['nacionalidad'])
            parentesco = Parentesco.objects.get(id_parentesco=data['parentesco'])
            tipo_apoderado = TipoApoderado.objects.get(nombre_tipo_apoderado=item[0].capitalize())
            nivel_academico = NivelAcademico.objects.get(id_nivel_academico=data['nivel_academico'])

            if data['vive_con_alumno']:
                direccion = Direccion.objects.get(id_direccion=alumno_persona.id_direccion.id_direccion)
            else:
                comuna = Comuna.objects.get(id_comuna=data['comuna'])
                direccion, _ = Direccion.objects.get_or_create(
                    nombre_calle = body['nombre_calle'],
                    numero = body['numero'],
                    id_comuna = comuna
                )

            persona, _ = Persona.objects.update_or_create(
                run = data['rut'],
                defaults={
                    'p_nombre': data['p_nombre'],
                    's_nombre': data['s_nombre'],
                    'appaterno': data['appaterno'],
                    'apmaterno': data['apmaterno'],
                    'fecha_nacimiento': data['fecha_nacimiento'],
                    'id_nacionalidad': nacionalidad,
                    'telefono_fijo': data['telefono_fijo'],
                    'celular': data['celular'],
                    'email': data['email'],
                    'id_direccion': direccion,
                    'id_genero': genero
                }
            )
            responsable, _ = Responsable.objects.update_or_create(
                run = persona,
                defaults={
                    'id_parentesco': parentesco,
                    'id_nivel_academico': nivel_academico,
                    'vive_con_alumno': data['vive_con_alumno']
                }
            )
            responsablealumno, _ = ResponsableAlumno.objects.update_or_create(
                run_responsable = responsable,
                defaults = {
                    'run_alumno': alumno_alumno,
                    'id_tipo_apoderado': tipo_apoderado
                }
            )

        return Response({ 'ok': True })
    except Exception as e:
        return Response({ 'ok': False, 'msg': str(e) })

## USUARIOS (PROFESORES)
@csrf_exempt
@api_view(['POST'])
def createTeacher(request):
    try:
        body = json.loads(json.dumps(request.data))
        comuna = Comuna.objects.get(id_comuna=body['comuna'])
        nacionalidad = Nacionalidad.objects.get(id_nacionalidad=body['nacionalidad'])
        genero = Genero.objects.get(id_genero=body['genero'])
        grado_academico = GradoAcademico.objects.get(id_grado_academico=body['grado_academico'])
        titulo = Titulo.objects.get(id_titulo=body['titulo'])
        mencion = Mencion.objects.get(id_mencion=body['mencion'])

        direccion, _ = Direccion.objects.get_or_create(
            nombre_calle = body['nombre_calle'],
            numero = body['numero'],
            id_comuna = comuna
        )
        persona, _ = Persona.objects.update_or_create(
            run = body['rut'],
            defaults = {
                'p_nombre': body['p_nombre'],
                's_nombre': body['s_nombre'],
                'appaterno': body['appaterno'],
                'apmaterno': body['apmaterno'],
                'fecha_nacimiento': body['fecha_nacimiento'],
                'id_nacionalidad': nacionalidad,
                'telefono_fijo': body['telefono_fijo'],
                'celular': body['celular'],
                'email': body['email'],
                'id_direccion': direccion,
                'id_genero': genero
            }
        )
        profesor, created = Profesor.objects.update_or_create(
            run = persona,
            defaults = {
                'id_grado_academico': grado_academico,
                'id_titulo': titulo,
                'id_mencion': mencion,
                'magister': body['magister'],
                'doctorado': body['doctorado']
            }
        )

        if created:
            msg = 'Profesor creado con exito.'
        else:
            msg = 'Informacion actualizada con exito.'
            
        messages.success(request, msg)
        return Response({ 'ok': True }, 200)
    except Exception as e:
        messages.error(request, str(e))
        return Response({ 'ok': False, 'msg': str(e) }, 500)

## USUARIOS (ADMINISTRADORES)
@csrf_exempt
@api_view(['POST'])
def createAdmin(request):
    try:
        body = json.loads(json.dumps(request.data))
        comuna = Comuna.objects.get(id_comuna=body['comuna'])
        nacionalidad = Nacionalidad.objects.get(id_nacionalidad=body['nacionalidad'])
        genero = Genero.objects.get(id_genero=body['genero'])
        grado_academico = GradoAcademico.objects.get(id_grado_academico=body['grado_academico'])
        titulo = Titulo.objects.get(id_titulo=body['titulo'])
        mencion = Mencion.objects.get(id_mencion=body['mencion'])
        cargo = Cargo.objects.get(id_cargo=body['cargo'])

        direccion, _ = Direccion.objects.get_or_create(
            nombre_calle = body['nombre_calle'],
            numero = body['numero'],
            id_comuna = comuna
        )
        persona, _ = Persona.objects.update_or_create(
            run = body['rut'],
            defaults = {
                'p_nombre': body['p_nombre'],
                's_nombre': body['s_nombre'],
                'appaterno': body['appaterno'],
                'apmaterno': body['apmaterno'],
                'fecha_nacimiento': body['fecha_nacimiento'],
                'id_nacionalidad': nacionalidad,
                'telefono_fijo': body['telefono_fijo'],
                'celular': body['celular'],
                'email': body['email'],
                'id_direccion': direccion,
                'id_genero': genero
            }
        )
        administrador, created = Administrador.objects.update_or_create(
            run = persona,
            defaults = {
                'id_grado_academico': grado_academico,
                'id_titulo': titulo,
                'id_mencion': mencion,
                'magister': body['magister'],
                'doctorado': body['doctorado'],
                'id_cargo': cargo
            }
        )

        if created:
            msg = 'Administrador creado con exito.'
        else:
            msg = 'Informacion actualizada con exito.'

        messages.success(request, msg)
        return Response({ 'ok': True }, 200)
    except Exception as e:
        messages.error(request, str(e))
        return Response({ 'ok': False, 'msg': str(e) }, 500)