# apps/api/router.py
from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.ventas.views import ProductosViewSet, ClienteViewSet, VentaViewSet
from apps.ventas.views_reportes import ReporteVentas

router = DefaultRouter()
router.register(r'productos', ProductosViewSet, basename='productos')
router.register(r'clientes', ClienteViewSet, basename='clientes')
router.register(r'ventas', VentaViewSet, basename='ventas')

urlpatterns = router.urls + [
    path('reportes/ventas/', ReporteVentas.as_view(), name='reporte-ventas'),
]
