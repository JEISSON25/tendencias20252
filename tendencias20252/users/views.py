from django.shortcuts import render
from .serializers import MovimientoUsuarioSerializer
from .models import MovimientoUsuario
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

class MovimientoUsuarioView(ListAPIView):
    queryset = MovimientoUsuario.objects.all().order_by('-fecha_actividad') 
    serializer_class = MovimientoUsuarioSerializer
    permission_classes = [IsAuthenticated] 
    