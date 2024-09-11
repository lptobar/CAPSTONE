# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractUser
from django.db import models

class Alumno(models.Model):
    run = models.OneToOneField('Persona', models.PROTECT, primary_key=True, db_column='run')
    rut_padre = models.ForeignKey('Persona', models.PROTECT, null=True, related_name='rut_padre_set')
    rut_madre = models.ForeignKey('Persona', models.PROTECT, null=True, related_name='rut_madre_set')
    id_estado_alumno = models.ForeignKey('EstadoAlumno', models.PROTECT, db_column='id_estado_alumno')
    estudiante_prioritario = models.BooleanField(default=False)
    enfermedad_cronica = models.CharField(max_length=255, null=True)
    seguro_escolar_particular = models.CharField(max_length=255, null=True)
    discapacidad_fisica = models.CharField(max_length=255, null=True)
    evaluacion_profesional = models.BooleanField(default=False)
    colegio_procedencia = models.CharField(max_length=255, null=True)
    razon_cambio_colegio = models.CharField(max_length=255, null=True)
    medio = models.CharField(max_length=255, null=True)
    pie = models.BooleanField(default=False)

    def __str__(self):
        return str(f'{self.run.p_nombre} {self.run.s_nombre} {self.run.appaterno} {self.run.apmaterno}')

class Region(models.Model):
    id_region = models.AutoField(primary_key=True)
    nombre_region = models.CharField(max_length=255)

class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    nombre_comuna = models.CharField(max_length=255)
    id_region = models.ForeignKey('Region', models.PROTECT, db_column='id_region')

class Jornada(models.Model):
    id_jornada = models.AutoField(primary_key=True)
    nombre_jornada = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_jornada

class Curso(models.Model):
    id_curso = models.CharField(primary_key=True, max_length=45, verbose_name='Código Curso')
    anio_curso = models.CharField(max_length=4, verbose_name='Año')
    id_lista_curso = models.ForeignKey('ListaCurso', models.PROTECT, db_column='id_lista_curso', verbose_name='Lista de Cursos')
    id_tipo_curso = models.ForeignKey('TipoCurso', models.PROTECT, db_column='id_tipo_curso', verbose_name='Tipo Curso')
    id_jornada = models.ForeignKey('Jornada', models.PROTECT, db_column='id_jornada',verbose_name='Tipo Jornada')
    profesor_jefe = models.ForeignKey('Profesor', models.PROTECT, db_column='run_profesor_jefe')
    id_estado_curso = models.ForeignKey('EstadoCurso', models.PROTECT, db_column='id_estado_curso')
    matriculas_disponibles = models.IntegerField()

    def __str__(self):
        return f'{ self.id_lista_curso.nombre_curso } { self.id_tipo_curso.nombre_tipo_curso } - { self.id_jornada.nombre_jornada }'

class CursoRepetido(models.Model):
    id_curso_repetido = models.AutoField(primary_key=True)
    id_lista_curso = models.ForeignKey('Curso', models.PROTECT, db_column='id_lista_curso')
    anno_repitencia = models.IntegerField()
    run_alumno = models.ForeignKey('Alumno', models.PROTECT, db_column='run_alumno')

class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    nombre_calle = models.CharField(max_length=255)
    numero = models.IntegerField()
    id_comuna = models.ForeignKey('Comuna', models.PROTECT, db_column='id_comuna')

class EstadoAlumno(models.Model):
    id_estado_alumno = models.AutoField(primary_key=True)
    nombre_estado_alumno = models.CharField(max_length=255)

class EstadoMatricula(models.Model):
    id_estado_matricula = models.AutoField(primary_key=True)
    nombre_estado_matricula = models.CharField(max_length=255)

class EstadoUsuario(models.Model):
    id_estado_usuario = models.AutoField(primary_key=True)
    nombre_estado_usuario = models.CharField(max_length=255)

class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True)
    nombre_genero = models.CharField(max_length=255)

class GrupoFamiliar(models.Model):
    id_grupo_familiar = models.AutoField(primary_key=True)
    nombre_familiar = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    id_parentesco = models.ForeignKey('Parentesco', models.PROTECT, db_column='id_parentesco')
    run_alumno = models.ForeignKey('Alumno', models.PROTECT, db_column='run_alumno')

class ListaCurso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    nombre_curso = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_curso

class Matricula(models.Model):
    id_matricula = models.CharField(primary_key=True, max_length=50)
    id_estado_matricula = models.ForeignKey('EstadoMatricula', models.PROTECT, db_column='id_estado_matricula')
    id_curso_matricula = models.ForeignKey('Curso', models.PROTECT, db_column='id_curso_matricula', related_name='set_curso_matricula')
    run_alumno = models.ForeignKey('Alumno', models.PROTECT, db_column='run_alumno')
    id_ultimo_curso_aprobado = models.ForeignKey('ListaCurso', models.PROTECT, null=True, db_column='id_ultimo_curso_aprobado', related_name='set_ultimo_curso_aprobado')

class Parentesco(models.Model):
    id_parentesco = models.AutoField(primary_key=True)
    nombre_parentesco = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_parentesco

class Nacionalidad(models.Model):
    id_nacionalidad = models.AutoField(primary_key=True)
    nombre_nacionalidad = models.CharField(max_length=50)

class Persona(models.Model):
    run = models.CharField(primary_key=True, max_length=10)
    p_nombre = models.CharField(max_length=255)
    s_nombre = models.CharField(max_length=255, blank=True)
    appaterno = models.CharField(max_length=255)
    apmaterno = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    id_nacionalidad = models.ForeignKey('Nacionalidad', models.PROTECT, db_column='id_nacionalidad')
    telefono_fijo = models.BigIntegerField()
    celular = models.BigIntegerField()
    email = models.CharField(max_length=255, null=True)
    id_direccion = models.ForeignKey('Direccion', models.PROTECT, db_column='id_direccion')
    id_genero = models.ForeignKey('Genero', models.PROTECT, db_column='id_genero')

    def __str__(self):
        return self.run

class Profesor(models.Model):
    run = models.OneToOneField('Persona', models.PROTECT, primary_key=True, db_column='run', to_field='run')
    id_grado_academico = models.ForeignKey('GradoAcademico', models.PROTECT, db_column='id_grado_academico')
    id_titulo = models.ForeignKey('Titulo', models.PROTECT, db_column='id_titulo')
    id_mencion = models.ForeignKey('Mencion', models.PROTECT, db_column='id_mencion')
    magister = models.CharField(max_length=50, null=True)
    doctorado = models.CharField(max_length=50, null=True)

    def __str__(self):
        return str(f'{self.run.p_nombre} {self.run.s_nombre} {self.run.appaterno} {self.run.apmaterno}')
    
class Responsable(models.Model):
    run = models.OneToOneField('Persona', models.PROTECT, primary_key=True, db_column='run', to_field='run')
    id_nivel_academico = models.ForeignKey('NivelAcademico', models.PROTECT, db_column='id_nivel_academico')
    vive_con_alumno = models.BooleanField()
    id_parentesco = models.ForeignKey('Parentesco', models.PROTECT, db_column='id_parentesco')

class ResponsableAlumno(models.Model):
    id_responsable_alumno = models.AutoField(primary_key=True)
    run_responsable = models.ForeignKey('Responsable', models.PROTECT, db_column='run_responsable', related_name='set_run_responsable')
    run_alumno = models.ForeignKey('Alumno', models.PROTECT, db_column='run_alumno', related_name='set_run_alumno')
    id_tipo_apoderado = models.ForeignKey('TipoApoderado', models.PROTECT, db_column='id_tipo_apoderado')

class TipoApoderado(models.Model):
    id_tipo_apoderado = models.AutoField(primary_key=True)
    nombre_tipo_apoderado = models.CharField(max_length=255)

class TipoCurso(models.Model):
    id_tipo_curso = models.AutoField(primary_key=True)
    nombre_tipo_curso = models.CharField(max_length=2)

    def __str__(self):
        return self.nombre_tipo_curso

class TipoUsuario(models.Model):
    id_tipo_usuario = models.AutoField(primary_key=True)
    nombre_tipo_usuario = models.CharField(max_length=255)

class Usuario(AbstractUser):
    id_usuario = models.CharField(primary_key=True, max_length=12)
    password = models.CharField(max_length=255)
    id_tipo_usuario = models.ForeignKey('TipoUsuario', models.PROTECT, db_column='id_tipo_usuario')
    id_estado_usuario = models.ForeignKey('EstadoUsuario', models.PROTECT, db_column='id_estado_usuario')    

class TipoAsistencia(models.Model):
    id_tipo_asistencia = models.AutoField(primary_key=True)
    nombre_tipo_asistencia = models.CharField(max_length=30)

class AsistenciaCurso(models.Model):
    id_asistencia_curso = models.CharField(primary_key=True, max_length=50)
    fecha_asistencia = models.DateField()
    id_curso = models.ForeignKey('Curso', models.PROTECT, db_column='id_curso')
    run_alumno = models.ForeignKey('Alumno', models.PROTECT, db_column='run_alumno')
    id_tipo_asistencia = models.ForeignKey('TipoAsistencia', models.PROTECT, db_column='id_tipo_asistencia')

class ListaAsignatura(models.Model):
    id_lista_asignatura = models.AutoField(primary_key=True)
    nombre_lista_asignatura = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_lista_asignatura

class Asignatura(models.Model):
    id_asignatura = models.CharField(primary_key=True, max_length=30)
    id_lista_asignatura = models.ForeignKey('ListaAsignatura', models.PROTECT, db_column='id_lista_asignatura')
    id_curso = models.ForeignKey('Curso', models.PROTECT, db_column='id_curso')
    run_profesor = models.ForeignKey('Profesor', models.PROTECT, db_column='run_profesor')

class Notas(models.Model):
    id_nota = models.AutoField(primary_key=True)
    nota = models.FloatField()
    id_asignatura = models.ForeignKey('Asignatura', models.PROTECT, db_column='id_asignatura')
    run_alumno = models.ForeignKey('Alumno', models.PROTECT, db_column='run_alumno', related_name='notas')

class TipoAnotacion(models.Model):
    id_tipo_anotacion = models.AutoField(primary_key=True)
    nombre_tipo_anotacion = models.CharField(max_length=20)

    def __str__(self):
        return str(self.nombre_tipo_anotacion)

class Anotacion(models.Model):
    id_anotacion = models.AutoField(primary_key=True)
    anotacion = models.CharField(max_length=200)
    fecha_anotacion = models.DateField()
    id_asignatura = models.ForeignKey('Asignatura', models.PROTECT, db_column='id_asignatura')
    id_tipo_anotacion = models.ForeignKey('TipoAnotacion', models.PROTECT, db_column='id_tipo_anotacion')
    run_alumno = models.ForeignKey('Alumno', models.PROTECT, db_column='run_alumno')

class Administrador(models.Model):
    run = models.OneToOneField('Persona', models.PROTECT, primary_key=True, db_column='run', to_field='run')
    id_grado_academico = models.ForeignKey('GradoAcademico', models.PROTECT, db_column='id_grado_academico')
    id_titulo = models.ForeignKey('Titulo', models.PROTECT, db_column='id_titulo')
    id_mencion = models.ForeignKey('Mencion', models.PROTECT, db_column='id_mencion')
    magister = models.CharField(max_length=50, null=True)
    doctorado = models.CharField(max_length=50, null=True)
    id_cargo = models.ForeignKey('Cargo', models.PROTECT, db_column='id_cargo')

class TipoNoticia(models.Model):
    id_tipo_noticia = models.AutoField(primary_key=True)
    nombre_tipo_noticia = models.CharField(max_length=20)

    def __str__(self):
        return str(self.nombre_tipo_noticia)

class PrioridadNoticia(models.Model):
    id_prioridad_noticia = models.AutoField(primary_key=True)
    nombre_prioridad_noticia = models.CharField(max_length=20)

    def __str__(self):
        return str(self.nombre_prioridad_noticia)

class Noticia(models.Model):
    id_noticia = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    subtitulo = models.CharField(max_length=255)
    cuerpo = models.TextField()
    fecha_noticia = models.DateField()
    id_tipo_noticia = models.ForeignKey('TipoNoticia', models.PROTECT, db_column='id_tipo_noticia')
    id_prioridad_noticia = models.ForeignKey('PrioridadNoticia', models.PROTECT, db_column='id_prioridad_noticia')
    imagen = models.ImageField(upload_to='media/noticias/')

class EstadoMensualidad(models.Model):
    id_estado_mensualidad=models.AutoField(primary_key=True)
    nombre_estado_mensualidad=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.nombre_estado_mensualidad)
    
class TipoMensualidad(models.Model):
    id_tipo_mensualidad=models.AutoField(primary_key=True)
    nombre_tipo_mesualidad=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.nombre_tipo_mesualidad)
    
class Mensualidades(models.Model):
    id_mensualidad = models.AutoField(primary_key=True)
    id_matricula = models.ForeignKey('Matricula',models.PROTECT,db_column='id_matricula')
    monto_mensualidad = models.IntegerField()
    id_tipo_mensualidad = models.ForeignKey('TipoMensualidad',models.PROTECT,db_column='id_tipo_mensualidad')
    id_estado_mensualidad = models.ForeignKey('EstadoMensualidad',models.PROTECT,db_column='id_estado_mensualidad')
    fecha_vencimiento = models.DateField()

class NivelAcademico(models.Model):
    id_nivel_academico = models.AutoField(primary_key=True)
    nombre_nivel_academico = models.CharField(max_length=50)

class GradoAcademico(models.Model):
    id_grado_academico = models.AutoField(primary_key=True)
    nombre_grado_academico = models.CharField(max_length=50)

class Titulo(models.Model):
    id_titulo = models.AutoField(primary_key=True)
    nombre_titulo = models.CharField(max_length=50)

class Mencion(models.Model):
    id_mencion = models.AutoField(primary_key=True)
    nombre_mencion = models.CharField(max_length=50)

class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    nombre_cargo = models.CharField(max_length=50)

class EstadoCurso(models.Model):
    id_estado_curso = models.AutoField(primary_key=True)
    nombre_estado_curso = models.CharField(max_length=50)