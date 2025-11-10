from rest_framework import viewsets, generics, permissions, filters, authentication
from .models import Usuarios
from ..roles.models import Roles
from .serializers import UsuariosSerializer, RegisterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


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


# --- Vista inicial ---
def initial_view(request):
    if request.user.is_authenticated:
        if request.user.rol == 'Admin':
            return redirect('home')
        elif request.user.rol == 'employee':
            return redirect('home')
        else:
            return redirect('home')
    return redirect('login')


# --- Vista de login con template ---
def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user.rol)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')


# --- Vista principal protegida ---
def home_view(request):
    return render(request, 'home.html')


def usuarios_view(request):
    return render(request, 'usuarios.html')