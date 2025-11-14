from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, filters, authentication
from .models import Usuarios
from apps.logs.utils import crear_log
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

    def perform_update(self, serializer):
        usuario_editado = serializer.save()
        crear_log(
            usuario=self.request.user,
            status="success",
            level="usuarios",
            message=f"Editó el usuario: {usuario_editado.username}"
        )

    def perform_destroy(self, instance):
        crear_log(
            usuario=self.request.user,
            status="warning",
            level="usuarios",
            message=f"Eliminó el usuario: {instance.username}"
        )
        instance.delete()


# --- API para registro (abierto) ---
class RegisterView(generics.CreateAPIView):
    queryset = Usuarios.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def perform_create(self, serializer):
        new_user = serializer.save()
        crear_log(
            usuario=new_user, # El  usuario que se registra
            status="success",
            level="registro",
            message=f"El usuario {new_user.username} se registró"
        )

def usuarios_view(request):
    return render(request, 'usuarios.html')
