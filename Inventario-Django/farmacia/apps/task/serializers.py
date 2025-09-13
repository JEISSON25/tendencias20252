from rest_framework import serializers
from .models import (
    Categoria,Producto,Proveedor,
    Cliente,Empleado,FacturaVenta,
    DetalleVenta,Movimiento
)

# ModelSerializer: es una clase de DRF que automatiza la creación de serializadores basados en modelos de Django.
# Meta es una subclase que centralizar la configuración y metadatos del serializador
# fields: define qué campos del modelo se incluyen en la serialización 

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Proveedor
        fields= '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'

class FacturaVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturaVenta
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'

class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimiento
        fields = '__all__'