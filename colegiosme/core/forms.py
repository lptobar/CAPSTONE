from dataclasses import fields

from django import forms
from .models import *
from datetime import datetime, date


class CursoForm(forms.ModelForm):

    id_curso = forms.CharField(label=False, initial='creandoId', widget=forms.TextInput(attrs={ 'disabled':'disabled' }))
    anio_select = [(str(year), str(year)) for year in range(datetime.now().year, datetime.now().year + 2)]

    anio_curso = forms.CharField(
        label = 'Año',
        widget = forms.Select(choices=anio_select)
    )
    class Meta:
        model = Curso
        fields = ['id_curso', 'id_lista_curso', 'id_tipo_curso', 'id_jornada', 'anio_curso', 'profesor_jefe', 'matriculas_disponibles']
    def __init__(self,*args,**kwargs):
        super(CursoForm,self).__init__(*args,**kwargs)
        self.fields['id_curso'].widget.attrs['class'] = 'ocultar'

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = '__all__'

class GrupoFamiliarForm(forms.ModelForm):
    run_alumno = forms.CharField(widget=forms.TextInput(attrs={ 'disabled': 'disabled' }))
    fecha_nacimiento = forms.CharField(widget=forms.TextInput(attrs={ 'type': 'date' }))
    
    class Meta:
        model = GrupoFamiliar
        fields = ('__all__')

class CursoRepetidoForm(forms.ModelForm):
    # run_alumno = forms.CharField(widget=forms.TextInput(attrs={ 'disabled': 'disabled' }))

    class Meta:
        model = CursoRepetido
        fields = ('__all__')    

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('__all__')    

class AnotacionForm(forms.ModelForm):
   
    class Meta:
        model=Anotacion
        fields=('__all__')

class AsignaturaForm(forms.ModelForm):

    class Meta:
        model=Asignatura
        fields=('id_asignatura', 'id_lista_asignatura', 'id_curso', 'run_profesor')
        widgets = {
            'id_asignatura': forms.HiddenInput(),  # Campo que deseas ocultar
        }

class AsistenciaCursoForm(forms.ModelForm):

    class Meta:
        model=AsistenciaCurso
        fields=('__all__')

class AnotacionForm(forms.ModelForm):
    #fecha_anotacion = forms.DateField(initial=date.today())
    fecha_anotacion = forms.DateField(initial=date.today(), widget=forms.DateInput(attrs={'disabled': 'disabled'}))
    id_asignatura = forms.ModelChoiceField(label='Asignatura', queryset=Asignatura.objects.all())

    class Meta:
        model = Anotacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        id = kwargs.pop('id', None)
        id_curso = kwargs.pop('id_curso', None)
        super(AnotacionForm, self).__init__(*args, **kwargs)
        #self.fields['run_alumno'] = forms.CharField(initial=id)
        self.fields['run_alumno'] = forms.CharField(widget=forms.HiddenInput(), initial=id)
        self.fields['fecha_anotacion'] = forms.DateField(widget=forms.HiddenInput(), initial=date.today())

        asignaturas = Asignatura.objects.filter(id_curso=id_curso)
        opciones_asignaturas = [(asignatura.id_asignatura, asignatura.id_lista_asignatura) for asignatura in asignaturas]
        self.fields['id_asignatura'].choices = opciones_asignaturas

    def clean_run_alumno(self):
        run = self.cleaned_data['run_alumno']
        try:
            alumno = Alumno.objects.get(run=run)
            return alumno
        except Alumno.DoesNotExist:
            raise forms.ValidationError("El alumno seleccionado no existe.")

class NoticiaForm(forms.ModelForm):
    fecha_noticia = forms.DateField(initial=date.today(), widget=forms.DateInput(attrs={'disabled': 'disabled'}))

    class Meta:
        model = Noticia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NoticiaForm, self).__init__(*args, **kwargs)
        self.fields['fecha_noticia'].widget = forms.HiddenInput()
        self.fields['fecha_noticia'].initial = date.today()
