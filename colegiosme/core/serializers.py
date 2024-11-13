from rest_framework import serializers
from .models import *

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'

class ReunionSerializer(serializers.ModelSerializer):
    destinatario = PersonaSerializer()

    class Meta:
        model = Reunion
        fields = '__all__'