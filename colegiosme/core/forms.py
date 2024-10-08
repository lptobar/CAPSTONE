from datetime import datetime, date
from django import forms
from .models import *

class AnotacionForm(forms.ModelForm):
    class Meta:
        model = Anotacion
        fields = ('descripcion_anotacion', 'tipo_anotacion')

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ('id_asignatura', 'lista_asignatura', 'curso', 'funcionario')
        widgets = {
            'id_asignatura': forms.HiddenInput(),  # Campo que deseas ocultar
        }

class CursoForm(forms.ModelForm):
    id_curso = forms.CharField(label=False, initial='creandoId', widget=forms.TextInput(attrs={ 'disabled':'disabled' }))
    anio_select = [(str(year), str(year)) for year in range(datetime.now().year, datetime.now().year + 2)]

    anio_curso = forms.CharField(
        label = 'Año',
        widget = forms.Select(choices=anio_select)
    )

    class Meta:
        model = Curso
        fields = ['id_curso', 'lista_curso', 'tipo_curso', 'jornada', 'anio_curso', 'funcionario', 'matriculas_disponibles']
        
    def __init__(self, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        self.fields['id_curso'].widget.attrs['class'] = 'ocultar'

class NoticiaForm(forms.ModelForm):
    fecha_noticia = forms.DateField(initial=date.today(), widget=forms.DateInput(attrs={'disabled': 'disabled'}))

    class Meta:
        model = Noticia
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NoticiaForm, self).__init__(*args, **kwargs)
        self.fields['fecha_noticia'].widget = forms.HiddenInput()
        self.fields['fecha_noticia'].initial = date.today()

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'

class TipoUsuarioForm(forms.ModelForm):
    tipo_usuario = forms.ModelChoiceField(
        queryset = TipoUsuario.objects.filter(id_tipo_usuario__gte=1),
        empty_label = 'Elige un tipo de usuario'
    )

    class Meta:
        model = TipoUsuario
        fields = ['tipo_usuario']