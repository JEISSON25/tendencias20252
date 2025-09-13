from rest_framework import viewsets #es un modulo de django que te permite crear vistas
#para Apis de manera rapida y con menos codigo

from .models import(
    Categoria,Producto,Proveedor,
    Cliente,Empleado,FacturaVenta,
    DetalleVenta,Movimiento
)
from .serializers import(
    CategoriaSerializer,ProductoSerializer,ProveedorSerializer,
    ClienteSerializer,EmpleadoSerializer,FacturaVentaSerializer,
    DetalleVentaSerializer,MovimientoSerializer
)
#ModeViewset  es una clase que proporciona automaticamente
#  todas las operaciones CRUD para un modelo de django

class CategoriaViewset(viewsets.ModelViewSet):
    queryset= Categoria.objects.all() #Define qué datos se van a mostrar o manipular.
    serializer_class = CategoriaSerializer #indica qué serializador usar para convertir los datos del modelo a JSON 

class ProductoViewset(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProveedorViewset(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ClienteViewset(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class EmpleadoViewset(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class FacturaVentaViewset(viewsets.ModelViewSet):
    queryset = FacturaVenta.objects.all()
    serializer_class = FacturaVentaSerializer

class DetalleVentaViewset(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

class MovimientoViewset(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
