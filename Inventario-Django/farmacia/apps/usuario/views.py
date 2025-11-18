from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
<<<<<<< HEAD
from .models import Usuario, Rol
from .serializers import (
    UsuarioSerializer,
    RolSerializer,
    CustomTokenObtainPairSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


=======
from .models import Usuario
from .serializers import UsuarioSerializer, CustomTokenObtainPairSerializer

# 🔹 Login JWT personalizado
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 🔹 CRUD de usuarios
>>>>>>> upstream/grupo5
class UsuarioViewset(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

<<<<<<< HEAD
class RolViewset(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewset, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewset)

urlpatterns = [
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),
]
>>>>>>> upstream/grupo5
