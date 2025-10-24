from rest_framework import viewsets, filters, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Productos, Cliente, Venta
from .serializers import ProductosSerializer, ClienteSerializer, VentaSerializer
from .permissions import IsAdminOrVendedorOrReadOnly, IsClienteOwnerOrReadOnly


class ProductosViewSet(viewsets.ModelViewSet):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'nombre', 'precio', 'stock']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = '__all__'


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'nombre', 'email', 'telefono']
    search_fields = ['nombre', 'email', 'telefono']
    ordering_fields = '__all__'
    permission_classes = [IsAdminOrVendedorOrReadOnly]


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.prefetch_related('detalles__producto', 'cliente').all()
    serializer_class = VentaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id', 'cliente', 'vendedor', 'fecha']
    search_fields = ['cliente__nombre', 'vendedor__username']
    ordering_fields = '__all__'
    permission_classes = [IsAdminOrVendedorOrReadOnly | IsClienteOwnerOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        # Los clientes solo ven sus propias ventas
        if user and user.is_authenticated and user.groups.filter(name='cliente').exists():
            return qs.filter(cliente__email=user.email)
        return qs

    def perform_create(self, serializer):
        """Asegura que solo usuarios autenticados creen ventas."""
        user = self.request.user
        if not user or not user.is_authenticated:
            raise permissions.exceptions.NotAuthenticated("Autenticación requerida para crear ventas.")
        serializer.save(vendedor=user)
