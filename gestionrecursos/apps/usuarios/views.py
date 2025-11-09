from rest_framework import viewsets
from .models import Usuarios
from ..roles.models import Roles
from .serializers import UsuariosSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] 
    filterset_fields = ('__all__')
    search_fields = ('__all__')
    ordering_fields = ('__all__')


# vista inicial
def initial_view(request):
    if request.user.is_authenticated:
         if request.user.rol == 'Admin':
             return redirect('home')
         elif request.user.rol == 'employee':
             return redirect('home')
         else:
             return redirect('home')

    return redirect('login')

#vista login
def login_view(request):
     if request.POST:
         username = request.POST['username']
         user = authenticate(request, username=username, password=request.POST['password'])
         if user is not None:
             login(request, user)
             print(user.rol)
             if user.rol == 'Admin':
                 return redirect('home')
             else:
                 return redirect('home')
         else:
             return render(request, 'login.html', {'error': 'Credenciales inválidas'})

     return render(request, 'login.html')


@login_required(login_url='/login/')
def home_view(request):
    return render(request, 'home.html')
 