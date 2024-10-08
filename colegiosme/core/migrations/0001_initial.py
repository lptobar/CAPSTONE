# Generated by Django 5.1.1 on 2024-10-08 14:24

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id_alumno', models.AutoField(primary_key=True, serialize=False)),
                ('alumno_prioritario', models.BooleanField(default=False)),
                ('enfermedad_cronica', models.CharField(blank=True, max_length=45)),
                ('discapacidad_fisica', models.CharField(blank=True, max_length=45)),
                ('seguro_escolar_particular', models.CharField(blank=True, max_length=45)),
                ('evaluacion_profesional', models.BooleanField(default=False)),
                ('colegio_procedencia', models.CharField(blank=True, max_length=45)),
                ('razon_cambio_colegio', models.CharField(blank=True, max_length=45)),
                ('medio_llego_colegio', models.CharField(blank=True, max_length=45)),
                ('pie', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='media/archivos_tareas/')),
            ],
        ),
        migrations.CreateModel(
            name='ArchivoEntrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='media/archivos_entrega/')),
            ],
        ),
        migrations.CreateModel(
            name='CargoFuncionario',
            fields=[
                ('id_cargo_funcionario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_cargo_funcionario', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id_comuna', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_comuna', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoAlumno',
            fields=[
                ('id_estado_alumno', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_estado_alumno', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoCurso',
            fields=[
                ('id_estado_curso', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_estado_curso', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoMatricula',
            fields=[
                ('id_estado_matricula', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_estado_matricula', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoMensualidad',
            fields=[
                ('id_estado_mensualidad', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_estado_mensualidad', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id_genero', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_genero', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Jornada',
            fields=[
                ('id_jornada', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_jornada', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ListaAsignatura',
            fields=[
                ('id_lista_asignatura', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_asignatura', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='ListaCurso',
            fields=[
                ('id_lista_curso', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_curso', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Nacionalidad',
            fields=[
                ('id_nacionalidad', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_nacionalidad', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='NivelAcademico',
            fields=[
                ('id_nivel_academico', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_nivel_academico', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Parentesco',
            fields=[
                ('id_parentesco', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_parentesco', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='PrioridadNoticia',
            fields=[
                ('id_prioridad_noticia', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_prioridad_noticia', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id_region', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_region', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TipoAnotacion',
            fields=[
                ('id_tipo_anotacion', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tipo_anotacion', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TipoAsistencia',
            fields=[
                ('id_tipo_asistencia', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tipo_asistencia', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='TipoCurso',
            fields=[
                ('id_letra_curso', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tipo_curso', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='TipoEspecializacion',
            fields=[
                ('id_tipo_especializacion', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_especializacion', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='TipoMensualidad',
            fields=[
                ('id_tipo_mensualidad', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tipo_mensualidad', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='TipoNoticia',
            fields=[
                ('id_tipo_noticia', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tipo_noticia', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('id_tipo_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_tipo_usuario', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='EntregaTarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.TextField(blank=True)),
                ('fecha_entrega', models.DateTimeField(default=django.utils.timezone.now)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.alumno')),
                ('archivos', models.ManyToManyField(blank=True, to='core.archivoentrega')),
            ],
        ),
        migrations.AddField(
            model_name='archivoentrega',
            name='entrega',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.entregatarea'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='estado_alumno',
            field=models.ForeignKey(db_column='id_estado_alumno', on_delete=django.db.models.deletion.PROTECT, to='core.estadoalumno'),
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id_funcionario', models.AutoField(primary_key=True, serialize=False)),
                ('cargo_funcionario', models.ForeignKey(db_column='id_cargo_funcionario', on_delete=django.db.models.deletion.PROTECT, to='core.cargofuncionario')),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id_curso', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('anio_curso', models.IntegerField()),
                ('matriculas_disponibles', models.IntegerField()),
                ('estado_curso', models.ForeignKey(db_column='id_estado_curso', default=2, on_delete=django.db.models.deletion.PROTECT, to='core.estadocurso')),
                ('funcionario', models.ForeignKey(db_column='id_profesor_jefe', on_delete=django.db.models.deletion.PROTECT, to='core.funcionario')),
                ('jornada', models.ForeignKey(db_column='id_jornada', on_delete=django.db.models.deletion.PROTECT, to='core.jornada')),
                ('lista_curso', models.ForeignKey(db_column='id_lista_curso', on_delete=django.db.models.deletion.PROTECT, to='core.listacurso')),
                ('tipo_curso', models.ForeignKey(db_column='id_tipo_curso', on_delete=django.db.models.deletion.PROTECT, to='core.tipocurso')),
            ],
        ),
        migrations.CreateModel(
            name='FuncionarioEspecializacion',
            fields=[
                ('id_funcionario_especializacion', models.AutoField(primary_key=True, serialize=False)),
                ('funcionario', models.ForeignKey(db_column='id_funcionario', on_delete=django.db.models.deletion.PROTECT, to='core.funcionario')),
            ],
        ),
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id_asignatura', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('curso', models.ForeignKey(db_column='id_curso', on_delete=django.db.models.deletion.PROTECT, to='core.curso')),
                ('funcionario', models.ForeignKey(db_column='id_funcionario', on_delete=django.db.models.deletion.PROTECT, to='core.funcionario')),
                ('lista_asignatura', models.ForeignKey(db_column='id_lista_asignatura', on_delete=django.db.models.deletion.PROTECT, to='core.listaasignatura')),
            ],
        ),
        migrations.CreateModel(
            name='Matricula',
            fields=[
                ('id_matricula', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('ultimo_curso_aprobado', models.CharField(max_length=40)),
                ('fecha_matricula', models.DateField()),
                ('alumno', models.ForeignKey(db_column='id_alumno', on_delete=django.db.models.deletion.PROTECT, to='core.alumno')),
                ('curso', models.ForeignKey(db_column='id_curso', on_delete=django.db.models.deletion.PROTECT, to='core.curso')),
                ('estado_matricula', models.ForeignKey(db_column='id_estado_matricula', on_delete=django.db.models.deletion.PROTECT, to='core.estadomatricula')),
            ],
        ),
        migrations.CreateModel(
            name='Apoderado',
            fields=[
                ('id_apoderado', models.AutoField(primary_key=True, serialize=False)),
                ('nivel_academico', models.ForeignKey(db_column='id_nivel_academico', on_delete=django.db.models.deletion.PROTECT, to='core.nivelacademico')),
            ],
        ),
        migrations.CreateModel(
            name='Notas',
            fields=[
                ('id_notas', models.AutoField(primary_key=True, serialize=False)),
                ('nota', models.FloatField()),
                ('lista_asignatura', models.ForeignKey(db_column='id_lista_asignatura', on_delete=django.db.models.deletion.PROTECT, to='core.listaasignatura')),
                ('matricula', models.ForeignKey(db_column='id_matricula', on_delete=django.db.models.deletion.PROTECT, to='core.matricula')),
            ],
        ),
        migrations.CreateModel(
            name='GrupoFamiliar',
            fields=[
                ('id_grupo_familiar', models.AutoField(primary_key=True, serialize=False)),
                ('es_responsable', models.BooleanField()),
                ('alumno', models.ForeignKey(db_column='id_alumno', on_delete=django.db.models.deletion.PROTECT, to='core.alumno')),
                ('apoderado', models.ForeignKey(db_column='id_apoderado', on_delete=django.db.models.deletion.PROTECT, to='core.apoderado')),
                ('parentesco', models.ForeignKey(db_column='id_parentesco', on_delete=django.db.models.deletion.PROTECT, to='core.parentesco')),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id_persona', models.AutoField(primary_key=True, serialize=False)),
                ('rut', models.BigIntegerField()),
                ('p_nombre', models.CharField(max_length=40)),
                ('s_nombre', models.CharField(blank=True, max_length=40)),
                ('ap_paterno', models.CharField(max_length=40)),
                ('ap_materno', models.CharField(max_length=40)),
                ('email', models.CharField(max_length=45)),
                ('genero', models.ForeignKey(db_column='id_genero', on_delete=django.db.models.deletion.PROTECT, to='core.genero')),
                ('nacionalidad', models.ForeignKey(db_column='id_nacionalidad', on_delete=django.db.models.deletion.PROTECT, to='core.nacionalidad')),
            ],
        ),
        migrations.AddField(
            model_name='funcionario',
            name='persona',
            field=models.ForeignKey(db_column='id_persona', on_delete=django.db.models.deletion.PROTECT, to='core.persona'),
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id_direccion', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_calle', models.CharField(max_length=45)),
                ('numero', models.IntegerField()),
                ('departamento', models.CharField(blank=True, max_length=45)),
                ('comuna', models.ForeignKey(db_column='id_comuna', on_delete=django.db.models.deletion.PROTECT, to='core.comuna')),
                ('persona', models.ForeignKey(db_column='id_persona', on_delete=django.db.models.deletion.PROTECT, to='core.persona')),
            ],
        ),
        migrations.AddField(
            model_name='apoderado',
            name='persona',
            field=models.ForeignKey(db_column='id_persona', on_delete=django.db.models.deletion.PROTECT, to='core.persona'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='persona',
            field=models.ForeignKey(db_column='id_persona', on_delete=django.db.models.deletion.PROTECT, to='core.persona'),
        ),
        migrations.AddField(
            model_name='comuna',
            name='region',
            field=models.ForeignKey(db_column='id_region', on_delete=django.db.models.deletion.PROTECT, to='core.region'),
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id_tarea', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha_fin', models.DateTimeField()),
                ('archivos', models.ManyToManyField(blank=True, db_column='archivos', related_name='archivos_tareas', to='core.archivo')),
                ('asignatura', models.ForeignKey(db_column='id_asignatura', on_delete=django.db.models.deletion.PROTECT, to='core.asignatura')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.curso')),
                ('funcionario', models.ForeignKey(db_column='profesor', on_delete=django.db.models.deletion.PROTECT, to='core.funcionario')),
            ],
        ),
        migrations.AddField(
            model_name='entregatarea',
            name='tarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tarea'),
        ),
        migrations.AddField(
            model_name='archivo',
            name='tarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.tarea'),
        ),
        migrations.CreateModel(
            name='Anotacion',
            fields=[
                ('id_anotacion', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion_anotacion', models.TextField()),
                ('fecha_anotacion', models.DateField(default=django.utils.timezone.now)),
                ('lista_asignatura', models.ForeignKey(db_column='id_lista_asignatura', on_delete=django.db.models.deletion.PROTECT, to='core.listaasignatura')),
                ('matricula', models.ForeignKey(db_column='id_matricula', on_delete=django.db.models.deletion.PROTECT, to='core.matricula')),
                ('tipo_anotacion', models.ForeignKey(db_column='id_tipo_anotacion', on_delete=django.db.models.deletion.PROTECT, to='core.tipoanotacion')),
            ],
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id_asistencia', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_asistencia', models.DateField()),
                ('alumno', models.ForeignKey(db_column='id_alumno', on_delete=django.db.models.deletion.PROTECT, to='core.alumno')),
                ('curso', models.ForeignKey(db_column='id_curso', on_delete=django.db.models.deletion.PROTECT, to='core.curso')),
                ('tipo_asistencia', models.ForeignKey(db_column='id_tipo_asistencia', on_delete=django.db.models.deletion.PROTECT, to='core.tipoasistencia')),
            ],
        ),
        migrations.CreateModel(
            name='Especializacion',
            fields=[
                ('id_especializacion', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_especializacion', models.CharField(max_length=45)),
                ('tipo_especializacion', models.ForeignKey(db_column='id_tipo_especializacion', on_delete=django.db.models.deletion.PROTECT, to='core.tipoespecializacion')),
            ],
        ),
        migrations.CreateModel(
            name='Mensualidad',
            fields=[
                ('id_mensualidad', models.AutoField(primary_key=True, serialize=False)),
                ('monto_total', models.IntegerField()),
                ('fecha_vencimiento', models.DateField()),
                ('estado_mensualidad', models.ForeignKey(db_column='id_estado_mensualidad', on_delete=django.db.models.deletion.PROTECT, to='core.estadomensualidad')),
                ('matricula', models.ForeignKey(db_column='id_matricula', on_delete=django.db.models.deletion.PROTECT, to='core.matricula')),
                ('tipo_mensualidad', models.ForeignKey(db_column='id_tipo_mensualidad', on_delete=django.db.models.deletion.PROTECT, to='core.tipomensualidad')),
            ],
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id_noticia', models.AutoField(primary_key=True, serialize=False)),
                ('titulo_noticia', models.CharField(max_length=45)),
                ('subtitulo_noticia', models.CharField(max_length=45)),
                ('cuerpo_noticia', models.CharField(max_length=45)),
                ('fecha_noticia', models.DateField()),
                ('imagen_noticia', models.ImageField(upload_to='media/noticias/')),
                ('funcionario', models.ForeignKey(db_column='id_funcionario', on_delete=django.db.models.deletion.PROTECT, to='core.funcionario')),
                ('prioridad_noticia', models.ForeignKey(db_column='id_prioridad_noticia', on_delete=django.db.models.deletion.PROTECT, to='core.prioridadnoticia')),
                ('tipo_noticia', models.ForeignKey(db_column='id_tipo_noticia', on_delete=django.db.models.deletion.PROTECT, to='core.tiponoticia')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('persona', models.ForeignKey(db_column='id_persona', on_delete=django.db.models.deletion.PROTECT, to='core.persona')),
                ('tipo_usuario', models.ForeignKey(db_column='id_tipo_usuario', on_delete=django.db.models.deletion.PROTECT, to='core.tipousuario')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
