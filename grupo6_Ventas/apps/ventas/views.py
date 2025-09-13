from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Productos, Cliente
from .serializers import ProductosSerializer, ClienteSerializer


class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer  
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'nombre', 'precio', 'stock']
    search_fields = ['nombre', 'descripcion', 'categoria__nombre']
    ordering_fields = '__all__' 

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'nombre', 'email', 'telefono', 'productos']
    search_fields = ['nombre', 'email', 'telefono', 'productos__nombre']
    ordering_fields = '__all__'
