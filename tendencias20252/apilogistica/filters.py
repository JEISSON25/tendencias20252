# filters.py

from django_filters import rest_framework as filters
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

class ProductosFilter(filters.FilterSet):
    class Meta:
        model = Productos
        fields = {
            'producto_referencia': ['exact'],
            'producto_nombre': ['icontains'],
            'marca': ['icontains'],
            'precio_ponderado': ['gt', 'lt'],
        }

class AsociadoFilter(filters.FilterSet):
    class Meta:
        model = Asociado
        fields = {
            'cedula_Asociado': ['exact'],
            'nombre_Asociado': ['icontains'],
            'cuidad': ['exact'],
            'Zona': ['exact'],
        }

class FacturasContabilidadFilter(filters.FilterSet):
    class Meta:
        model = Facturas_contabilidad
        fields = {
            'origen': ['exact'],
            'fecha_factura': ['exact', 'gt', 'lt'],
            'cedula_Asociado': ['exact'],
            'vendedor': ['exact'],
            'estado_orden': ['exact'],
            'conductor': ['exact'],
        }

class ListaProductosPedidosFilter(filters.FilterSet):
    class Meta:
        model = Lista_productos_pedidos
        fields = {
            'producto_referencia': ['exact'],
            'origen': ['exact'],
        }

class ListaProductosNegadosFilter(filters.FilterSet):
    class Meta:
        model = Lista_productos_negados
        fields = {
            'producto_referencia': ['exact'],
            'origen': ['exact'],
        }
        
# --- Las clases corregidas están a continuación ---

# Nombre y clase padre corregidos
class OrigenFilter(filters.FilterSet):
    class Meta: 
        model = Origen
        fields = {
            'origen': ['exact']
        }

# Nombre y clase padre corregidos
class ZonaFilter(filters.FilterSet):
    class Meta: 
        model = Zona
        fields = {
            'zona': ['exact']
        }

# Clase padre corregida
class CuidadFilter(filters.FilterSet):
    class Meta: 
        model = Cuidad
        fields = {
            'cuidad': ['exact']
        }

# Clase padre corregida
class ConductorFilter(filters.FilterSet):
    class Meta: 
        model = Conductor
        fields = {
            'conductor': ['exact']
        }
        
# Clase padre y modelo corregidos
class VendedorFilter(filters.FilterSet):
    class Meta: 
        model = Vendedor # Esto debe ser el modelo Vendedor
        fields = {
            'vendedor': ['exact'] # Esto debe ser el campo 'vendedor'
        }