from rest_framework import serializers
from .models import Recursos

class RecursosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recursos
        fields = '__all__'
