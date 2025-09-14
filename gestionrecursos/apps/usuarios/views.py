from rest_framework import viewsets
from .models import Usuarios
from .serializers import UsuariosSerializer

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer
