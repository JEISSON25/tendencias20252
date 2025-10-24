# urls.py de tu aplicación

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrigenViewSet,
    ProductosViewSet,
    ListaProductosNegadosViewSet,
    ListaProductosPedidosViewSet,
    CuidadViewSet,
    ZonaViewSet,
    AsociadoViewSet,
    VendedorViewSet,
    ConductorViewSet,
    FacturasContabilidadViewSet
)

# 1. Crea una instancia del router
router = DefaultRouter()

# 2. Registra cada ViewSet con su URL base
router.register(r'origenes', OrigenViewSet)
router.register(r'productos', ProductosViewSet)
router.register(r'listas-productos-negados', ListaProductosNegadosViewSet)
router.register(r'listas-productos-pedidos', ListaProductosPedidosViewSet)
router.register(r'ciudades', CuidadViewSet)
router.register(r'zonas', ZonaViewSet)
router.register(r'asociados', AsociadoViewSet)
router.register(r'vendedores', VendedorViewSet)
router.register(r'conductores', ConductorViewSet)
router.register(r'facturas-contabilidad', FacturasContabilidadViewSet)

urlpatterns = [
   
    path("v1/", include(router.urls)),
]