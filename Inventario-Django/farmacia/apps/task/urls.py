#Aqui Definimos  las rutas relacionadas con los modelos y vistas de la aplicación task.
#Mantenemos  el código limpio y modular, separando las URLs por aplicación.

#path: Para crear rutas individuales.
#include: Para incluir otras rutas (como las de DRF).
from django.urls import path, include
from rest_framework.routers import DefaultRouter #Es un "administrador de rutas" que automáticamente genera las URLs para las ViewSets
from .views import (
    CategoriaViewset,ProductoViewset,ProveedorViewset,
    ClienteViewset,EmpleadoViewset,FacturaVentaViewset,
    DetalleVentaViewset,MovimientoViewset
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewset, basename='categoria')
router.register(r'productos', ProductoViewset, basename='producto')
router.register(r'proveedores', ProveedorViewset, basename='proveedor')
router.register(r'clientes', ClienteViewset, basename='cliente')
router.register(r'empleados', EmpleadoViewset, basename='empleado')
router.register(r'facturasventa', FacturaVentaViewset, basename='facturaventa')
router.register(r'detallesventa', DetalleVentaViewset, basename='detalleventa')
router.register(r'movimientos', MovimientoViewset, basename='movimiento')

urlpatterns =[
    path('',include(router.urls))
]
#