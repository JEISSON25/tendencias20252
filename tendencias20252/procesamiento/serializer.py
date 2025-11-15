from rest_framework import serializers
from .models import ProductoNegado, pickingModel, CortesLogistico

class CortesLogisticoSerializer (serializers.ModelSerializer):
    class Meta:
        model = CortesLogistico
        fields = '__all__'

class ProductoNegadoSerializer(serializers.ModelSerializer):
    fecha = serializers.DateField(format="%Y-%m-%d") # Asegura el formato ISO estándar
    cantidad_negada = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        model = ProductoNegado
        fields = '__all__'
        

class PickingSerializer(serializers.ModelSerializer):
    nombrecorte = serializers.PrimaryKeyRelatedField(
        queryset=CortesLogistico.objects.all())
    
    class Meta:
        model = pickingModel
        fields = '__all__'
        



class PickingPatchSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True) 
    producto = serializers.CharField(max_length=1000, required=False) 
    cantidad = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    pesoUnitario = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = pickingModel
        fields = ['id', 'nombreAsociado', 'vendedor', 'cantidad', 'producto', 'pesoUnitario', 'cuidad', 'codigoZona', 'zona', 'origen', 'marca', 'idOdoo'] 
        
        extra_kwargs = {
            'nombreAsociado': {'required': False},
            'vendedor': {'required': False},
            'cantidad': {'required': False},
            'producto': {'required': False},
            'pesoUnitario': {'required': False},
            'cuidad': {'required': False},
            'codigoZona': {'required': False},
            'zona': {'required': False},
            'origen': {'required': False},
            'marca': {'required': False},
            'idOdoo': {'required': False},
        }
        
        