from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, filters, authentication
from .models import Usuarios
from ..roles.models import Roles
from .serializers import UsuariosSerializer, RegisterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

# --- API para gestionar usuarios (solo autenticados) ---
class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('__all__')
    search_fields = ('__all__')
    ordering_fields = ('__all__')


# --- API para registro (abierto) ---
class RegisterView(generics.CreateAPIView):
    queryset = Usuarios.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

def usuarios_view(request):
    return render(request, 'usuarios.html')
