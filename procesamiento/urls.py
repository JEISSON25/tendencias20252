# urls.py de tu aplicación

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductoNegadoViewSet,
    UploadExcelProductoNegadoView,
    ReporteNegadosView  
)

# 1. Crea una instancia del router
router = DefaultRouter()

# 2. Registra cada ViewSet con su URL base
router.register(r'productoNegado', ProductoNegadoViewSet)
router.register(r'UploadExcelProductoNegado', UploadExcelProductoNegadoView)
router.register(r'ReporteNegados', ReporteNegadosView)

urlpatterns = [
   
    path("procesamiento/", include(router.urls)),
]