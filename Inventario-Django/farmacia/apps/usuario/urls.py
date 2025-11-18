from django.urls import path
from .views import CustomTokenObtainPairView
<<<<<<< HEAD
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewset, basename='usuario')
router.register(r'roles', RolViewset, basename='roles')

urlpatterns = router.urls
=======

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain'),
]
>>>>>>> upstream/grupo5
