from rest_framework import serializers
from .models import ProductoNegado, pickingModel

class ProductoNegadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoNegado
        fields = '__all__'
        

class PickingSerializer(serializers.ModelSerializer):
    class Meta:
        model = pickingModel
        fields = '__all__'