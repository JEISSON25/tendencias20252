
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovimientoUsuarioView

# 1. Crea una instancia del router
router = DefaultRouter()


urlpatterns = [
    path('usuarios_movimientos/', MovimientoUsuarioView.as_view(), name='movimientos_usuario')
]
