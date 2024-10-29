from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from datetime import date
from .models import *
from .forms import *
import json
from django.http import QueryDict
from django.contrib import messages
from django.db.models import Max, Sum, Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view
from rest_framework.response import Response
from transbank.webpay.webpay_plus.transaction import Transaction
from .carro import Carro
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.db import IntegrityError

import random

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse, JsonResponse

# Create your views here.
def home(request):
    data = {
        'noticias': Noticia.objects.all()
    }

    #persona = Persona(pk=5)
    #tipo = TipoUsuario(pk=3)
    #Usuario.objects.create_user(username='sergio', password='1234', persona=persona, tipo_usuario=tipo)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, 'Inicio de sesión correcto, bienvenido!')
            login(request, user)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos, intente nuevamente.')

    return render(request, 'index.html', data)

def cerrar_sesion(request):
    logout(request)
    
    return redirect('inicio')

## -- ANOTACIONES -- ##
def anotaciones_asignaturas(request):
    data = {
        'asignaturas': Asignatura.objects.filter(funcionario__persona__rut=request.user.persona.rut)
    }

    return render(request, 'anotaciones/anotaciones-asignaturas.html', data)

def anotaciones_estudiantes(request, id):
    data = {
        'asignatura': Asignatura.objects.get(id_asignatura=id),
        'tipo_anotaciones': TipoAnotacion.objects.all(),
        'alumnos': []
    }

    matriculas = Matricula.objects.filter(curso=data['asignatura'].curso)
    for matricula in matriculas:
        anotaciones = Anotacion.objects.filter(lista_asignatura=data['asignatura'].lista_asignatura, matricula=matricula)
        data['alumnos'].append({ 'alumno': matricula.alumno, 'anotaciones': anotaciones })

    return render(request, 'anotaciones/anotaciones-estudiantes.html', data)

def portal_anotaciones(request):
    grupo_familiar = GrupoFamiliar.objects.filter(apoderado__persona__rut=request.user.persona.rut)
    alumno_ids = grupo_familiar.values_list('alumno__id_alumno', flat=True)
    
    data = {
        'alumnos': Alumno.objects.filter(id_alumno__in=alumno_ids)
    }

    return render(request, 'anotaciones/portal-anotaciones.html', data)

def ver_anotaciones(request, id):
    matricula = Matricula.objects.get(alumno__persona__rut=id, estado_matricula__id_estado_matricula=1)
    asignaturas = Asignatura.objects.filter(curso=matricula.curso)
    tipo_anotaciones = TipoAnotacion.objects.all()

    data = {
        'alumno': matricula.alumno,
        'tipo_anotaciones': tipo_anotaciones,
        'anotaciones': []
    }

    for asignatura in asignaturas:
        anotaciones = Anotacion.objects.filter(matricula__alumno__persona__rut=id)
        data['anotaciones'].append({ 'asignatura': asignatura, 'anotaciones': anotaciones })
    
    return render(request, 'anotaciones/ver-anotaciones.html', data)

def crear_anotacion(request, id):
    url_anterior = request.META.get('HTTP_REFERER')
    matricula = Matricula.objects.get(alumno__persona__rut=id, estado_matricula=1)
    curso = Curso.objects.get(id_curso=matricula.curso.id_curso)
    alumno = Alumno.objects.get(persona__rut=matricula.alumno.persona.rut)
    persona = Persona.objects.get(rut=alumno.persona.rut)

    formulario = AnotacionForm()

    if request.method == 'POST':
        formulario = AnotacionForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            pass
        else:
            pass

    data = {
        'fecha': date.today(),
        'curso': curso,
        'formulario': formulario,
        'persona': persona
    }

    return render(request, 'anotaciones/crear-anotaciones.html', data)

## -- NOTAS -- ##
def portal_notas_profesor(request):
    asignaturas = Asignatura.objects.filter(funcionario__persona=request.user.persona)

    data = {
        'asignaturas': []
    }

    for asignatura in asignaturas:
        notas = Notas.objects.filter(lista_asignatura=asignatura.lista_asignatura).values_list('nota', flat=True)
        data['asignaturas'].append({ 'asignatura': asignatura, 'notas': list(notas) })

    return render(request, 'notas/portal-notas-profesor.html', data)

def notas_asignatura(request, id):
    asignatura = Asignatura.objects.get(pk=id)
    matriculas = Matricula.objects.filter(curso=asignatura.curso, estado_matricula=1)
    notas_max_id = Notas.objects.order_by('-id_notas').first()
    notas_max_id = notas_max_id.id_notas if notas_max_id is not None else 0

    data = {
        'url_anterior': request.META.get('HTTP_REFERER'),
        'alumnos': []
    }

    for matricula in matriculas:
        notas = Notas.objects.filter(matricula=matricula, lista_asignatura=asignatura.lista_asignatura)
        notas_max_id += 1

        data['alumnos'].append({ 'alumno': matricula.alumno, 'notas': notas, 'nota_max_id': notas_max_id })

    if request.method == 'POST':
        for name, value in request.POST.items():
            if name == 'csrfmiddlewaretoken' or value == '0':
                continue

            rut, id_nota = name.split('nota')
            Notas.objects.update_or_create(
                id_notas = id_nota,
                defaults = {
                    'nota': float(value.replace(',', '.')),
                    'lista_asignatura': asignatura.lista_asignatura,
                    'matricula': Matricula.objects.get(alumno__persona__rut=rut)
                }
            )
        
        return redirect('portal-notas-profesor')

    return render(request, 'notas/notas-asignatura.html', data)

def notas_curso(request, id=None):
    cursos = Curso.objects.all()
    data = {
        'cursos': cursos,
        'asignaturas': []
    }

    if id is not None:
        asignaturas = Asignatura.objects.filter(curso__id_curso=id)

        for asignatura in asignaturas:
            notas = Notas.objects.filter(lista_asignatura=asignatura.lista_asignatura).values_list('nota', flat=True)
            promedio = 0.0 if len(notas) == 0 else round(sum(notas) / len(notas), 1)
            data['asignaturas'].append({ 'asignatura': asignatura, 'promedio': promedio })

    return render(request, 'notas/notas-curso.html', data)

def portal_notas_apoderado(request):
    grupo_familiar = GrupoFamiliar.objects.filter(apoderado__persona__rut=request.user.persona.rut)
    alumno_ids = grupo_familiar.values_list('alumno__id_alumno', flat=True)
    
    data = {
        'alumnos': Alumno.objects.filter(id_alumno__in=alumno_ids)
    }

    return render(request, 'notas/portal-notas-apoderado.html', data)

def notas_estudiante(request, id):
    matricula = Matricula.objects.get(alumno__persona__rut=id)
    asignaturas = Asignatura.objects.filter(curso=matricula.curso)

    data = {
        'alumno': matricula.alumno,
        'asignaturas': [],
        'promedio_total': 0
    }

    for asignatura in asignaturas:
        notas = Notas.objects.filter(matricula__alumno=matricula.alumno, lista_asignatura=asignatura.lista_asignatura).values_list('nota', flat=True)
        promedio = 0.0 if len(notas) == 0 else round(sum(notas) / len(notas), 1)
        data['asignaturas'].append({ 'asignatura': asignatura, 'notas': notas, 'promedio': promedio })

    promedios = [d['promedio'] for d in data['asignaturas'] if d['promedio'] != 0.0]
    data['promedio_total'] = 0.0 if len(promedios) == 0 else round(sum(promedios) / len(promedios), 1)

    return render(request, 'notas/notas-estudiante.html', data)

## -- INFORMES -- ##
def informe_notas_estudiante(request, id):
    # Obtiene la plantilla HTML que se utilizará para generar el PDF
    template = get_template('informes/informe-notas-estudiante.html')

    # Renderiza la plantilla con los datos necesario
    matricula = Matricula.objects.get(alumno__persona__rut=id, estado_matricula__id_estado_matricula=1)
    curso = Curso.objects.get(id_curso=matricula.curso.id_curso)
    asignaturas = Asignatura.objects.filter(curso=matricula.curso)
    data = {
        'alumno': matricula.alumno,
        'curso': curso,
        'asignaturas': [],
        'promedio_total': 0
    }

    for asignatura in asignaturas:
        notas = Notas.objects.filter(matricula=matricula, lista_asignatura=asignatura.lista_asignatura).values_list('nota', flat=True)
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

def informe_matricula(request, id):
    template = get_template('informes/informe-matricula.html')

    # Renderiza la plantilla con los datos necesario
    matricula = Matricula.objects.get(pk=id)
    curso = Curso.objects.get(pk=matricula.curso.id_curso)
    alumno = Alumno.objects.get(pk=matricula.alumno)
    persona = Persona.objects.get(pk=alumno.persona.id_persona)
    responsables = GrupoFamiliar.objects.filter(alumno=matricula.alumno)

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

def informe_aprobados(request, id):
    template = get_template('informes/informe-aprobados.html')

    curso = Curso.objects.get(pk=id)
    matriculas = Matricula.objects.filter(curso=curso)

    data = {
        'curso': curso,
        'alumnos': []
    }

    for matricula in matriculas:
        alumno = Alumno.objects.get(pk=matricula.alumno.id_alumno)
        asignaturas = Asignatura.objects.filter(curso=curso)
        notas = Notas.objects.filter(matricula=matricula).values_list('nota', flat=True)
        promedio_final = 0.0 if len(notas) == 0 else round(sum(notas) / len(notas), 1)

        contador = 0
        for asignatura in asignaturas:
            notas = Notas.objects.filter(matricula=matricula, lista_asignatura=asignatura.lista_asignatura).values_list('nota', flat=True)
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

## -- ASISTENCIA -- ##
def portal_asistencia(request):
    grupo_familiar = GrupoFamiliar.objects.filter(apoderado__persona__rut=request.user.persona.rut)
    alumno_ids = grupo_familiar.values_list('alumno__id_alumno', flat=True)
    
    data = {
        'alumnos': Alumno.objects.filter(id_alumno__in=alumno_ids)
    }

    return render(request, 'asistencia/portal-asistencia.html', data)

def asistencia_estudiante(request, id):
    alumno = Alumno.objects.get(persona__rut=id)
    dataTotal = {
        'Alumno': alumno,
        'Total_Asistencias': Asistencia.objects.filter(alumno=alumno).count(),
        'Total_Inasistencia': Asistencia.objects.filter(alumno=alumno, tipo_asistencia__id_tipo_asistencia=1).count(),
        'Total_Asistencia': Asistencia.objects.filter(alumno=alumno, tipo_asistencia__id_tipo_asistencia=2).count(),
        'Total_Justificado':Asistencia.objects.filter(alumno=alumno, tipo_asistencia__id_tipo_asistencia=3).count()
    }
    datos = {
        'text': f'Asistencia del Alumno: { dataTotal["Alumno"].persona }',
        'subtext': 'Asistencia total: ' + str(dataTotal['Total_Asistencias']),
        'data': [{ 'value': dataTotal['Total_Asistencia'], 'name': 'Presentes' },
                { 'value': dataTotal['Total_Inasistencia'], 'name': 'Ausentes' },
                { 'value': dataTotal['Total_Justificado'], 'name': 'Justificado' }]
    }
    
    datos_json = json.dumps(datos)
    context = {
        'datos_json': datos_json, 
    }

    return render(request,'asistencia/asistencia-estudiante.html', context)

def asistencia_cursos(request):
    cursos = Curso.objects.all()
    fecha_actual = date.today().strftime('%d-%m-%Y')

    data = {
        'cursos': cursos,
        'fecha': fecha_actual
    }

    return render(request, 'asistencia/asistencia-cursos.html', data)

def registrar_asistencia(request, id):
    curso = Curso.objects.get(id_curso=id)
    matriculas = Matricula.objects.filter(curso__id_curso=id)
    alumnos = Alumno.objects.all()

    fecha_actual = date.today()
    fecha_actual = fecha_actual.strftime("%d-%m-%Y")

    alumnos_asistencia = []

    run_alumnos = alumnos.values_list('persona__rut', flat=True)
    alumnos_asistencia = alumnos.filter(persona__rut__in=run_alumnos)

    data = {
        
        'curso': curso,
        'matriculas': matriculas,
        'alumnos': alumnos_asistencia,
        'fecha': fecha_actual
    }

    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                if key.startswith('asistencia_'):
                    alumno_id = key.replace('asistencia_', '')
                    asistencia = value

                    # Guardar los datos en la base de datos
                    asistencia_obj = Asistencia()
                    asistencia_obj.fecha_asistencia = date.today()
                    asistencia_obj.curso = curso
                    alumno = Alumno.objects.get(persona__rut=alumno_id)
                    asistencia_obj.alumno = alumno
                    tipoAsistencia = TipoAsistencia.objects.get(id_tipo_asistencia=int(asistencia))
                    asistencia_obj.tipo_asistencia = tipoAsistencia

                    #asistencia_obj.id_asistencia_curso = f"{asistencia_obj.run_alumno.run}{asistencia_obj.id_curso.id_curso}{str(asistencia_obj.fecha_asistencia).replace('-','')}"
                    asistencia_obj.save()
            except ValueError as e:
                continue

        #messages.success(request, 'Registro de asistencias de alumno, curso: ' + id + ' guardada satifactoriamente...')
        return redirect(to="asistencia-cursos")
    
    return render(request, 'asistencia/registrar-asistencia.html', data)

def ver_asistencia_admin(request, id):
    curso = Curso.objects.get(id_curso=id)
    dataTotal = {
        'curso': curso,
        'total_asistencias': Asistencia.objects.filter(curso=curso).count(),
        'total_asistencia': Asistencia.objects.filter(curso=curso, tipo_asistencia__id_tipo_asistencia=1).count(),
        'total_inasistencia': Asistencia.objects.filter(curso=curso, tipo_asistencia__id_tipo_asistencia=2).count() + Asistencia.objects.filter(curso=curso, tipo_asistencia__id_tipo_asistencia=3).count()
    }
    datos = {'text': f'Asistencia del Curso: {dataTotal['curso']}',
           'subtext': 'Asistencia total :' + str(dataTotal['total_asistencias']),
           'data': [{'value': dataTotal['total_asistencia'], 'name': 'Presentes'},
                    {'value': dataTotal['total_inasistencia'], 'name': 'Ausentes'}
                   ]
            }
    array_alumnos = []
    array_asistencia = []
    array_inasistencia = []
    array_justificado = []
    matriculas = Matricula.objects.filter(curso=curso)

    for matricula in matriculas:
        persona = Persona.objects.get(rut=matricula.alumno.persona.rut)
        nombre = f'{persona.p_nombre} {persona.s_nombre} {persona.ap_paterno} {persona.ap_materno}'
        array_alumnos.append(nombre)
        
        presente = Asistencia.objects.filter(alumno=matricula.alumno, tipo_asistencia__id_tipo_asistencia=1).count()
        ausente = Asistencia.objects.filter(alumno=matricula.alumno, tipo_asistencia__id_tipo_asistencia=2).count()
        justificado = Asistencia.objects.filter(alumno=matricula.alumno, tipo_asistencia__id_tipo_asistencia=3).count()
        array_asistencia.append(presente)
        array_inasistencia.append(ausente)
        array_justificado.append(justificado)

    array_serie = [{
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
    }]

    datos_json3 = json.dumps(array_alumnos)
    datos_json2 = json.dumps(array_serie)
    datos_json = json.dumps(datos)
    context = {
        'datos_json':datos_json,
        'datos_json2':datos_json2,
        'datos_json3': datos_json3
    }
    return render(request,'asistencia/ver-asistencia-admin.html',context)

## -- CURSOS -- ##
def listar_cursos(request):
    cursos = Curso.objects.exclude(estado_curso=3)

    return render(request, 'cursos/listar-cursos.html', { 'cursos': cursos })

def crear_curso(request):
    data = {
        'formulario': CursoForm()
    }
    
    if request.method == 'POST':
        post_data = request.POST.copy()
        formulario = CursoForm(data=request.POST)
        if formulario.is_valid:
            try:
                lista_curso = ListaCurso.objects.get(pk=request.POST['lista_curso'])
                estado_curso = EstadoCurso.objects.get(pk=2)
                id_curso = f"{lista_curso.nombre_curso.replace(' ','')}{request.POST['anio_curso']}{request.POST['jornada']}{request.POST['tipo_curso']}"
                post_data['id_curso'] = id_curso
                post_data['id_estado_curso'] = estado_curso

                request.POST = QueryDict('', mutable=True)
                request.POST.update(post_data)

                formulario = CursoForm(data=request.POST)
                formulario.save()
                messages.success(request, f'El curso se creo correctamente id: {id_curso}')
            except ValueError as e:
                messages.error(request, f'Error al crear el curso el ID: {id_curso} ya existe.')
            except Exception as e:
                print(e)
                messages.error(request, 'Error en la Información')

            return redirect(to="listar-cursos")
        else:
            data["form"] = formulario

    return render(request, 'cursos/crear-curso.html', data)

def eliminar_curso(request, id):
    try:
        curso = Curso.objects.get(pk=id)
        matriculas = Matricula.objects.filter(curso=curso)
        
        if matriculas.exists():
            curso.estado_curso = EstadoCurso(pk=3)
        else:
            curso.delete()

        messages.success(request, f'Curso eliminado correctamente. ID: {id}')

        return redirect(to='listar-cursos')
    except Curso.DoesNotExist:
        messages.error(request, 'El curso no existe.')
        return redirect(to='listar-cursos')

def cerrar_curso(request, id):
    curso = Curso.objects.get(pk=id)
    estado_matricula = EstadoMatricula.objects.get(pk=2)
    estado_curso = EstadoCurso.objects.get(pk=2)
    matriculas = Matricula.objects.filter(curso=curso, estado_matricula__id_estado_matricula=1)

    for matricula in matriculas:
        matricula.estado_matricula = estado_matricula
        matricula.save()

    curso.estado_curso = estado_curso
    curso.save()

    return redirect(to=f'/informe-aprobados/{curso.id_curso}')

## -- ASIGNATURAS -- ##
def listar_asignaturas(request):
    cursos = Curso.objects.all()
    asignaturas = Asignatura.objects.all()

    data = {
        'cursos': cursos,
        'asignaturas': asignaturas
    }

    return render(request, 'asignaturas/listar-asignaturas.html', data)

def crear_asignatura(request):
    data = {
        'formulario': AsignaturaForm(),
    }

    if request.method == 'POST':
        post_data = request.POST.copy()
        formulario = CursoForm(data=request.POST)

        if formulario.is_valid:
            try:
                id_nuevoId = f"{request.POST['curso']}{request.POST['lista_asignatura']}{request.POST['funcionario']}"
                post_data['id_asignatura'] = id_nuevoId
                request.POST = QueryDict('',mutable=True)
                request.POST.update(post_data)
                formulario = AsignaturaForm(data=request.POST)
                formulario.save()
                messages.success(request, 'La asignatura se Creo correctamente id: ' + id_nuevoId)

                return redirect(to='listar-asignaturas')
            except ValueError as e:
                #messages.error(request, 'Error al crear la asignatura el ID: ' + id_nuevoId + ' ya existe')
                return redirect(to="listar-asignaturas")
        else:
            data["form"] = formulario

    return render(request, 'asignaturas/crear-asignatura.html', data)

def eliminar_asignatura(request, id):
    asignatura = Asignatura.objects.get(id_asignatura=id)
    asignatura.delete()

    return redirect(to="listar-asignaturas")

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    data = {
        'usuarios': usuarios,
    }

    return render(request, 'usuarios/listar-usuarios.html', data)

def crear_usuario(request):
    data = {
        'formulario_persona': PersonaForm(),
        'formulario_usuario': TipoUsuarioForm(),
    }

    if request.method == 'POST':
        formulario_persona = PersonaForm(data=request.POST)
        formulario_usuario = TipoUsuarioForm(data=request.POST)
        if formulario_persona.is_valid() and formulario_usuario.is_valid():
            tipo_usuario = formulario_usuario.cleaned_data['tipo_usuario']
            cargo_funcionario = CargoFuncionario.objects.get(nombre_cargo_funcionario=tipo_usuario.nombre_tipo_usuario)

            persona = formulario_persona.save()
            Funcionario.objects.create(cargo_funcionario=cargo_funcionario, persona=persona)
            Usuario.objects.create_user(
                username=f'{persona.p_nombre[:2].lower()}.{persona.ap_paterno.lower()}',
                password='1234',
                persona=persona,
                tipo_usuario=TipoUsuario(pk=tipo_usuario.id_tipo_usuario)
            )

            messages.success(request, 'Usuario creado con exito.')

        return redirect(to='listar-usuarios')

    return render(request, 'usuarios/crear-usuario.html', data)

def editar_usuario(request, id):
    data = {
        'formulario': PersonaForm(instance=Persona.objects.get(pk=id))
    }

    return render(request, 'usuarios/editar-usuario.html', data)

def eliminar_usuario(request, id):
    usuario = Usuario.objects.get(pk=id)
    usuario.delete()

    messages.success(request, 'Usuario eliminado con exito.')

    return redirect(to='listar-usuarios')

## -- MATRICULAS -- ##
def matricula_estudiante(request):
    nacionalidades = Nacionalidad.objects.all()
    generos = Genero.objects.all()
    cursos = Curso.objects.filter(~Q(anio_curso=str(datetime.now().year - 1)))

    data = {
        'cursos': cursos,
        'nacionalidades': nacionalidades,
        'generos': generos
    }

    return render(request, 'matricula/matricula-estudiante.html', data)

def matricula_padres(request, id):
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
                
        return render(request, 'matricula/matricula-padres.html', data)
    except Matricula.DoesNotExist:
        return redirect('inicio')

def matricula_apoderado(request, id):
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

@csrf_exempt
@api_view(['POST'])
def crear_matricula(request):
    try:
        body = json.loads(json.dumps(request.data))
        comuna = Comuna.objects.get(id_comuna=body['comuna'])
        nacionalidad = Nacionalidad.objects.get(id_nacionalidad=body['nacionalidad'])
        genero = Genero.objects.get(id_genero=body['genero'])
        estado_alumno = EstadoAlumno.objects.get(id_estado_alumno=1)
        curso = Curso.objects.get(id_curso=body['curso_matricula'])
        estado_matricula = EstadoMatricula.objects.get(id_estado_matricula=1)

        if curso.matriculas_disponibles < 0:
            return Response({ 'ok': False, 'msg': 'El curso no tiene cupos disponibles' })

        persona, _ = Persona.objects.update_or_create(
            rut = body['rut'],
            defaults = {
                'p_nombre': body['p_nombre'],
                's_nombre': body['s_nombre'],
                'ap_paterno': body['ap_paterno'],
                'ap_materno': body['ap_materno'],
                'nacionalidad': nacionalidad,
                'email': body['email'],
                'genero': genero
            }
        )
        alumno, _ = Alumno.objects.update_or_create(
            persona = persona,
            defaults = {
                'estado_alumno': estado_alumno,
            }
        )
        matricula, created = Matricula.objects.get_or_create(
            id_matricula = f'{body["curso_matricula"]}{body["rut"]}',
            defaults = {
                'fecha_matricula': date.today(),
                'alumno': alumno,
                'curso': curso,
                'estado_matricula': estado_matricula
            }
        )

        direccion, _ = Direccion.objects.get_or_create(
            nombre_calle = body['nombre_calle'],
            numero = body['numero'],
            comuna = comuna,
            persona = persona
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
    
## -- MENSUALIDADES -- ##
def listar_mensualidades(request):
    if request.user.tipo_usuario.id_tipo_usuario != 2:
        messages.error(request, 'Usuario no posee los atributos para acceder a esta página')
        return redirect(to='inicio')
    else:
        #responsable = ResponsableAlumno.objects.filter(run_responsable=user.username)
        matricula = Matricula.objects.all()
        mensualidad = Mensualidad.objects.all()
        data = {
            #'responsable': responsable,
            'matricula': matricula,
            'mensualidad': mensualidad
        }
       
    return render(request, 'mensualidad/mensualidad.html', data)

def agregar_mensualidad(request,id):
    carro = Carro(request)
    mensualidad = Mensualidad.objects.get(id_mensualidad=id)
    carro.agregar(mensualidad)

    return redirect(to='listarMensualidad')
    
def eliminar_mensualidad(request, id):
    carro = Carro(request)
    mensualidad = Mensualidad.objects.get(id_mensualidad=id)
    carro.eliminar(mensualidad)

    return redirect(to='listarMensualidad')

def restar_mensualidad(request, id):
    carro = Carro(request)
    mensualidad = Mensualidad.objects.get(id_mensualidad=id)
    carro.quitar(mensualidad)

    return redirect(to='ListarMensualidad')

## -- NOTICIAS -- ##
def crear_noticia(request):
    data = {
        'fecha': date.today(),
        'formulario': NoticiaForm()
    }

    if request.method == 'POST':
        formulario = NoticiaForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'La noticia se creó correctamente')

            return redirect('listar-noticias')
        else:
            for field, errors in formulario.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo {field}: {error}')

    return render(request, 'noticias/crear-noticia.html',data)

def listar_noticias(request):
    noticias = Noticia.objects.all()

    return render(request, 'noticias/listar-noticias.html', { 'noticias': noticias })

def ver_noticia(request, id):
    noticia = Noticia.objects.get(pk=id)
    noticias = Noticia.objects.exclude(pk=id)

    data = {
        'noticia': noticia,
        'noticias': noticias
    }

    return render(request, 'noticias/ver-noticia.html', data)

def editar_noticia(request, id):
    noticia = Noticia.objects.get(pk=id)
    data = {
        'formulario': NoticiaForm(instance=noticia)
    }

    if request.method == 'POST':
        formulario = NoticiaForm(data=request.POST, instance=noticia)

        if formulario.is_valid():
            formulario.save()
            return redirect('listar-noticias')
        
        data['form'] = formulario

    return render(request, 'noticias/editar-noticia.html', data)

def eliminar_noticia(request, id):
    noticia = Noticia.objects.get(pk=id)
    noticia.delete()
    messages.success(request, 'Noticia eliminada satifactoriamente')
    
    return redirect(to="listar-noticias")

## -- WEBPAY -- ##
def pago_webpay(request):
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
        return_url = 'http://127.0.0.1:8000/webpay-respuesta/'
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
def webpay_retorno(request):
    token = request.GET.get("token_ws")
    transaction = Transaction()
    response = transaction.commit(token=token)

    if response['status'] == 'AUTHORIZED':
        for key, value in request.session["carro"].items():
            id_mensualidad = int(value["id_mensualidad"])
            mensualidad = Mensualidad.objects.get(id_mensualidad=id_mensualidad)
            estado_mensualidad = EstadoMensualidad.objects.get(id_estado_mensualidad=2)
            mensualidad.id_estado_mensualidad=estado_mensualidad
            mensualidad.save()

        request.session["carro"] = {}
        request.session.modified = True

    return render (request, 'webpay/commit.html', { 'token': token, 'response': response })

## -- API HELPERS -- ##
@csrf_exempt
@api_view(['GET'])
def obtener_persona(request, rut):
    try:
        persona = Persona.objects.get(rut=rut)
        direccion = Direccion.objects.get(persona=persona)
        data = model_to_dict(persona)

        data['nombres'] = f'{data['p_nombre']} {data['s_nombre']}'
        data['nombre_calle'] = direccion.nombre_calle
        data['numero'] = direccion.numero
        data['region'] = direccion.comuna.region.nombre_region
        data['comuna'] = direccion.comuna.id_comuna

        print(data)

        return Response({ 'ok': True, 'data': data })
    except Exception as e:
        return Response({ 'ok': False, 'msg': e })

## --TAREA VISTA PROFESOR-- ##
def crear_tarea(request):
    profesor = Funcionario.objects.get(persona=request.user.persona)

    if request.method == 'POST':
        form = TareaForm(request.POST, request.FILES)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.funcionario = profesor
            tarea.save()
            
            # Manejo de archivos
            for archivo in request.FILES.getlist('archivos'):
                nuevo_archivo = Archivo.objects.create(archivo=archivo)
                tarea.archivos.add(nuevo_archivo) 

            messages.success(request, 'Tarea creada satifactoriamente')
            print(tarea.curso.id_curso)
            emails_alumnos, emails_apoderados = obtener_emails_curso(id_curso=tarea.curso.id_curso)
            asunto=f"Nueva Tarea {tarea.titulo}"
            mensaje=f"Hola,\n se informa que se acaba de subir una nueva tarea para la asignatura {tarea.asignatura} ,\n {tarea.descripcion},\n tiene plazo hasta {tarea.fecha_fin} para entregar la Tarea."
            enviar_correo(emails_alumnos,asunto,mensaje)
            enviar_correo(emails_apoderados,asunto,mensaje)
            return redirect('lista_tareas')
        else:
            messages.error(request, 'Tarea Error al intentar crear la tarea')
            print(form.errors)
            return redirect('lista_tareas')
    else:
        form = TareaForm()

    return render(request, 'tareas/crear_tarea.html', {'form': form})

def lista_tareas(request):
    profesor = Funcionario.objects.get(persona=request.user.persona)
    tareas = Tarea.objects.filter(funcionario=profesor)

    return render(request,'tareas/lista_tareas.html',{ 'tareas': tareas })

def ver_entrega_tarea(request, id_tarea):
    tarea=Tarea.objects.get(id_tarea=id_tarea)
    entregas=EntregaTarea.objects.filter(tarea=tarea)
   
    alumnos=Alumno.objects.filter(matricula__curso=tarea.curso)
    alumnos_entregaron=entregas.values_list('alumno',flat=True)
    return render(request,'tareas/ver_entregas_tarea.html',{
        'tarea':tarea,
        'entregas':entregas,
        'alumnos': alumnos,
        'alumnos_que_entregaron': alumnos_entregaron,

    })

def eliminar_tarea(request, id_tarea):
    tarea = Tarea.objects.get(id_tarea=id_tarea)
    tarea.delete()
    messages.success(request, 'Tarea eliminada satifactoriamente')
    
    return redirect(to="lista_tareas")

## --TAREA VISTA ALUMNO-- ##
def ver_tareas_alumno(request):
    alumno = Alumno.objects.get(persona=request.user.persona)
    matricula = Matricula.objects.get(alumno=alumno)
    tareas = Tarea.objects.filter(curso=matricula.curso)

    print(tareas)

    return render(request,'tareas/tareas_alumno.html', { 'tareas': tareas })

def entregar_tarea(request, id_tarea):
    tarea = Tarea.objects.get(id_tarea=id_tarea)
    alumno = Alumno.objects.get(persona=request.user.persona)

    if timezone.now() > tarea.fecha_fin:
        return redirect('tareas_alumno')

    if request.method == 'POST':
        form = EntregaTareaForm(request.POST, request.FILES)
        if form.is_valid():
            entrega = form.save(commit=False)
            entrega.tarea = tarea
            entrega.alumno = alumno
            entrega.save()
            
            # Guardar más de un archivo y asociarlo con la entrega
            for archivo in request.FILES.getlist('archivos'):
                nuevo_archivo = ArchivoEntrega.objects.create(archivo=archivo)
                entrega.archivos.add(nuevo_archivo)  # Asociar archivo con la entrega

            messages.success(request, 'Entrega de tarea satifactoriamente')

            email_alumno = alumno.persona.email
            email_profesor = tarea.funcionario.persona.email
            emails = [email_alumno, email_profesor]

            asunto = f"Entrega {alumno.persona} tarea: {tarea.titulo}"
            mensaje = f"Hola,\n se informa que se acaba de subir una entrega para la asignatura {tarea.asignatura} ,\n {tarea.descripcion},\n hora de entrega {date.today()}."
            enviar_correo(emails, asunto,mensaje)

            return redirect('tareas_alumno')
    else:
        form = EntregaTareaForm()
    return render(request, 'tareas/entregar_tarea.html', {'form': form, 'tarea': tarea})

def obtener_asignaturas(request, curso):
    profesor = Funcionario.objects.get(persona=request.user.persona)
    asignaturas= Asignatura.objects.filter(curso=curso, funcionario=profesor.id_funcionario)
    asignaturas_data = [{"id": asignatura.id_asignatura, "nombre": asignatura.lista_asignatura.nombre_asignatura} for asignatura in asignaturas]
    return JsonResponse(list(asignaturas_data), safe=False)

def obtener_asignaturas2(request, curso):
    asignaturas= Asignatura.objects.filter(curso=curso)
    asignaturas_data = [{"id": asignatura.id_asignatura, "nombre": asignatura.lista_asignatura.nombre_asignatura} for asignatura in asignaturas]
    return JsonResponse(list(asignaturas_data), safe=False)

def ver_mis_entregas(request, id_tarea):
    alumno = Alumno.objects.get(persona=request.user.persona)
    entregas = EntregaTarea.objects.filter(tarea=id_tarea, alumno=alumno)
    tarea = Tarea.objects.get(pk=id_tarea)

    data = {
        'entregas': entregas,
        'tarea': tarea
    }

    return render(request, 'tareas/ver_mis_tareas.html', data)

## --EMAIL-- ##
def enviar_correo( email,asunto,mensaje):
    print(asunto)
    print(mensaje)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = email
    data={
        'asunto' :asunto,
        'mensaje' :mensaje
    }
    print(data)
    # Renderizar la plantilla con contexto
    html_content = render_to_string('email/email.html',data)

    # Crear el email con el contenido HTML
    email_message = EmailMultiAlternatives(asunto, '', from_email, recipient_list)
    email_message.attach_alternative(html_content, "text/html")
    print("Contenido HTML generado:", html_content)
    email_message.send()

def obtener_emails_curso(id_curso):
    # Obtener el curso
    curso = Curso.objects.get(id_curso=id_curso)
    
    # Obtener todas las matrículas del curso
    matriculas = Matricula.objects.filter(curso=curso)
    
    # Listas para almacenar correos electrónicos
    emails_alumnos = []
    emails_apoderados = []

    for matricula in matriculas:
        # Obtener el alumno
        alumno = matricula.alumno
        # Obtener el email del alumno
        emails_alumnos.append(alumno.persona.email)
        
        # Obtener el apoderado del alumno desde el GrupoFamiliar
        grupo_familiar = GrupoFamiliar.objects.filter(alumno=alumno)
        
        # Obtener los emails de los apoderados relacionados
        for relacion in grupo_familiar:
            apoderado = relacion.apoderado
            emails_apoderados.append(apoderado.persona.email)

    return emails_alumnos, emails_apoderados

## --HORARIO-- ##
def listar_horarios(request):
    cursos = Curso.objects.all()
    return render(request, 'horario/listar_curso_horario.html', {'cursos': cursos})

def horario(request, id_curso):
    curso = Curso.objects.get(id_curso=id_curso)
    asignaturas = Asignatura.objects.filter(curso=curso)
    bloques = BloqueHorario.objects.all()  # Obtén todos los bloques horarios disponibles
    dias_semana = DiaSemana.objects.all()
    horarios_existentes = Horario.objects.filter(curso=curso)
    context = {
        'curso': curso,
        'asignaturas': asignaturas,
        'bloques': bloques,
        'dias_semana': dias_semana,
        'horario_existente':horarios_existentes,
    }
    
    return render(request, 'horario/crear_horario.html', context)

def asignar_asignatura(request):
    data = request.POST
    curso_id = data.get('curso_id')
    asignatura_id = data.get('asignatura_id')
    dia_id = data.get('dia_id')
    bloque_id = data.get('bloque_id')
    profesor_id = data.get('profesor_id')  # Obtén el ID del profesor responsable

    # Verificar si ya existe un horario para esta asignatura en este bloque y día para el mismo curso
    horario_existente = Horario.objects.filter(
        curso=curso_id,
        dia_semana=dia_id,
        bloque_horario=bloque_id
    ).first() 
     # Obtiene el primer registro si existe
    horario_utilizado=Horario.objects.filter(
        dia_semana=dia_id,
        bloque_horario=bloque_id,
        profesor=profesor_id
    ).first()
    try:
       
        if horario_existente:
            # Si existe, eliminar el registro anterior
            horario_existente.delete()  # Elimina el horario existente
        elif horario_utilizado:
            return JsonResponse({'status': 'error', 'message':'El profesor ya se encuentra asignado \n en este mismo horario y dia en otro curso'})
        # Crear un nuevo registro de horario
        horario = Horario.objects.create(
            curso_id=curso_id,
            asignatura_id=asignatura_id,
            dia_semana_id=dia_id,
            bloque_horario_id=bloque_id,
            profesor_id=profesor_id
        )
        return JsonResponse({'status': 'success', 'message': 'Asignatura asignada correctamente.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


## --Bloque Horario-- ##
def crear_bloque_horario(request):
    if request.method == 'POST':
        form = BloqueHorarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_bloques_horarios')  # Define esta URL para listar los bloques
    else:
        form = BloqueHorarioForm()
    return render(request, 'bloque_horario/crear_bloque_horario.html', {'form': form})

def listar_bloques_horarios(request):
    bloques = BloqueHorario.objects.all()
    return render(request, 'bloque_horario/listar_bloques_horarios.html', {'bloques': bloques})

def actualizar_bloque_horario(request, bloque_id):
    bloque = BloqueHorario.objects.get(pk=bloque_id)
    if request.method == 'POST':
        form = BloqueHorarioForm(request.POST, instance=bloque)
        if form.is_valid():
            form.save()
            return redirect('listar_bloques_horarios')
    else:
        form = BloqueHorarioForm(instance=bloque)
    return render(request, 'bloque_horario/actualizar_bloque_horario.html', {'form': form})

def eliminar_bloque_horario(request, bloque_id):
    bloque = BloqueHorario.objects.get(pk=bloque_id)
    bloque.delete()
    return redirect('listar_bloques_horarios')
    

