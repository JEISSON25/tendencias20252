# views.py

# views.py

from rest_framework import viewsets
from rest_framework import filters # <-- Los filtros de búsqueda y orden van aquí
from django_filters.rest_framework import DjangoFilterBackend # <-- El filtro de Django va aquí
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
from .serializer import (
    OrigenSerializer,
    ProductosSerializer,
    ListaProductosNegadosSerializer,
    ListaProductosPedidosSerializer,
    CuidadSerializer,
    ZonaSerializer,
    AsociadoSerializer,
    VendedorSerializer,
    ConductorSerializer,
    FacturasContabilidadSerializer
)
from .filters import (
    ProductosFilter,
    AsociadoFilter,
    FacturasContabilidadFilter,
    ListaProductosPedidosFilter,
    ListaProductosNegadosFilter,
    OrigenFilter,
    ZonaFilter,
    CuidadFilter,
    ConductorFilter,
    VendedorFilter
)



class OrigenViewSet(viewsets.ModelViewSet):
    queryset = Origen.objects.all()
    serializer_class = OrigenSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['origen']
    ordering_fields = ['id', 'origen']

class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductosFilter
    search_fields = ['producto_referencia', 'producto_nombre', 'marca']
    ordering_fields = ['producto_nombre', 'marca', 'precio_ponderado']

class ListaProductosNegadosViewSet(viewsets.ModelViewSet):
    queryset = Lista_productos_negados.objects.all()
    serializer_class = ListaProductosNegadosSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ListaProductosNegadosFilter

class ListaProductosPedidosViewSet(viewsets.ModelViewSet):
    queryset = Lista_productos_pedidos.objects.all()
    serializer_class = ListaProductosPedidosSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ListaProductosPedidosFilter

class CuidadViewSet(viewsets.ModelViewSet):
    queryset = Cuidad.objects.all()
    serializer_class = CuidadSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['cuidad']

class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['zona']

class AsociadoViewSet(viewsets.ModelViewSet):
    queryset = Asociado.objects.all()
    serializer_class = AsociadoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AsociadoFilter
    search_fields = ['cedula_Asociado', 'nombre_Asociado']
    ordering_fields = ['nombre_Asociado', 'cedula_Asociado']

class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['vendedor']

class ConductorViewSet(viewsets.ModelViewSet):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConductorFilter
    
class FacturasContabilidadViewSet(viewsets.ModelViewSet):
    queryset = Facturas_contabilidad.objects.all()
    serializer_class = FacturasContabilidadSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FacturasContabilidadFilter
    


