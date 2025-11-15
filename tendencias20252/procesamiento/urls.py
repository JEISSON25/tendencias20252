# urls.py de tu aplicación

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoNegadoViewSet,
    UploadExcelProductoNegadoView,
    UploadPickinView,
    ReporteDatosView,
    ActualizarPickingMasivoView, 
    CortesLogisticoView
)

# 1. Crea una instancia del router
router = DefaultRouter()

# 2. Registra cada ViewSet con su URL base
router.register(r'productoNegado', ProductoNegadoViewSet)


urlpatterns = [
   
    path("modelos/", include(router.urls)),
    path('upload_producto_negado/', UploadExcelProductoNegadoView.as_view(), name='upload-excel-producto-negado'),
    path('upload_picking_packing/', UploadPickinView.as_view(), name='upload-excel-picking-packing'),
    path('reporte_datos/', ReporteDatosView.as_view(), name='reporte-datos'),
    path("actualizar_picking_masivo/", ActualizarPickingMasivoView.as_view(), name = 'update-picking'),
    path("crear_corte/", CortesLogisticoView.as_view(), name = "create_corte")
]