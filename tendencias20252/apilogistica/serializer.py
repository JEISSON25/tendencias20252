# serializers.py

from rest_framework import serializers
from .models import (
    Origen,
    Productos,
    Lista_productos_negados,
    Lista_productos_pedidos,
    Cuidad,
    Zona,
    Asociado,
    Vendedor,
    Conductor,
    Facturas_contabilidad
)

# Serializadores simples para los modelos que no tienen relaciones complejas
class OrigenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Origen
        fields = '__all__'

class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = '__all__'

class ListaProductosNegadosSerializer(serializers.ModelSerializer):
    producto_referencia = ProductosSerializer()
    origen = OrigenSerializer()

    class Meta:
        model = Lista_productos_negados
        fields = '__all__'

class ListaProductosPedidosSerializer(serializers.Serializer):
    producto_referencia = ProductosSerializer()
    origen = OrigenSerializer()
    class Meta:
        model = Lista_productos_pedidos
        fields = '__all__'

class CuidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuidad
        fields = '__all__'

class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = '__all__'
        
class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'

class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = '__all__'


class AsociadoSerializer(serializers.ModelSerializer):
    cuidad = CuidadSerializer()
    Zona = ZonaSerializer()

    class Meta:
        model = Asociado
        fields = '__all__'


class FacturasContabilidadSerializer(serializers.ModelSerializer):
    origen = OrigenSerializer()
    cedula_Asociado = AsociadoSerializer()
    vendedor = VendedorSerializer()
    conductor = ConductorSerializer()
    
    class Meta:
        model = Facturas_contabilidad
        fields = '__all__'