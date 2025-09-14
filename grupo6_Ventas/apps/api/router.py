from rest_framework.routers import DefaultRouter
from ..ventas.views import *

router = DefaultRouter()

router.register(r'productos', ProductosViewSet, basename='Productos')
router.register(r'cliente', ClienteViewSet, basename='Cliente')

urlpatterns = router.urls