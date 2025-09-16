from rest_framework import serializers
from .models import ProductoNegado

class ProductoNegadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoNegado
        fields = '__all__'
        

