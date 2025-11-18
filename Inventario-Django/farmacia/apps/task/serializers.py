from rest_framework import serializers
from .models import *
from ..usuario.models import Usuario, Rol

<<<<<<< HEAD
# -----------------------------
# CATEGORÍA
# -----------------------------


=======
>>>>>>> upstream/grupo5
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

<<<<<<< HEAD

# -----------------------------
# PRODUCTO
# -----------------------------
class ProductoSerializer(serializers.ModelSerializer):
    low_stock = serializers.ReadOnlyField()
=======
class ProductoSerializer(serializers.ModelSerializer):
    low_stock = serializers.ReadOnlyField()  
>>>>>>> upstream/grupo5

    class Meta:
        model = Producto
        fields = '__all__'

<<<<<<< HEAD

# -----------------------------
# PROVEEDOR
# -----------------------------
=======
>>>>>>> upstream/grupo5
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

<<<<<<< HEAD

class ClienteSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all()
    )

    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'telefono', 'correo', 'usuario']
class EmpleadoSerializer(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all()
    )

    class Meta:
        model = Empleado
        fields = ['id', 'nombre', 'telefono', 'usuario']



# -----------------------------
# DETALLE VENTA
# -----------------------------
class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(
        source='id_producto.nombre', read_only=True)
    factura_fecha = serializers.DateField(
        source='id_factura.fecha', read_only=True)

=======
class ClienteSerializer(serializers.ModelSerializer):
    usuario = serializers.DictField(write_only=True)

    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'correo', 'telefono', 'usuario']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        rol_cliente, _ = Rol.objects.get_or_create(name='cliente')
        usuario = Usuario.objects.create_user(
            username=usuario_data['username'],
            password=usuario_data['password'],
            rol=rol_cliente
        )
        return Cliente.objects.create(usuario=usuario, **validated_data)
    
class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'
        
    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        rol_empleado, _ = Rol.objects.get_or_create(name='empleado')  # â† Ya no hay error
        usuario = Usuario.objects.create_user(
            username=usuario_data['username'],
            password=usuario_data['password'],
            rol=rol_empleado
        )
        return Empleado.objects.create(usuario=usuario, **validated_data)

class DetalleVentaSerializer(serializers.ModelSerializer):
    
    producto_nombre = serializers.CharField(source='id_producto.nombre', read_only=True)
    factura_fecha = serializers.DateField(source='id_factura.fecha', read_only=True)
    
>>>>>>> upstream/grupo5
    class Meta:
        model = DetalleVenta
        fields = '__all__'


<<<<<<< HEAD
# -----------------------------
# FACTURA VENTA
# -----------------------------
class FacturaVentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = FacturaVenta
        fields = ['id', 'fecha', 'total',
                  'id_cliente', 'id_empleado', 'detalles']
=======
class FacturaVentaSerializer(serializers.ModelSerializer):

    class Meta:
        model = FacturaVenta
        fields = '__all__'
>>>>>>> upstream/grupo5
        read_only_fields = ['fecha', 'total']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        factura = FacturaVenta.objects.create(**validated_data)
<<<<<<< HEAD

        total_factura = 0

        for item in detalles_data:
            detalle = DetalleVenta.objects.create(id_factura=factura, **item)
            total_factura += detalle.subtotal

        factura.total = total_factura
        factura.save()

        return factura


# -----------------------------
# MOVIMIENTO
# -----------------------------
class MovimientoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(
        source='id_producto.nombre', read_only=True)
    proveedor_nombre = serializers.CharField(
        source='id_proveedor.nombre', read_only=True)
    cliente_nombre = serializers.CharField(
        source='id_cliente.nombre', read_only=True)
    responsable_nombre = serializers.CharField(
        source='responsable.nombre', read_only=True)

=======
        for item in detalles_data:
            DetalleVenta.objects.create(id_factura=factura, **item)  
        return factura

class MovimientoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='id_producto.nombre', read_only=True)
    proveedor_nombre = serializers.CharField(source='id_proveedor.nombre', read_only=True)
    cliente_nombre = serializers.CharField(source='id_cliente.nombre', read_only=True)
    responsable_nombre = serializers.CharField(source='responsable.nombre', read_only=True)
    
>>>>>>> upstream/grupo5
    class Meta:
        model = Movimiento
        fields = '__all__'

    def validate(self, data):
<<<<<<< HEAD

        if data['tipo'] == 'entrada' and not data.get('id_proveedor'):
            raise serializers.ValidationError(
                "Para entradas, debe especificar un proveedor."
            )

        if data['tipo'] == 'salida' and not data.get('id_cliente'):
            raise serializers.ValidationError(
                "Para salidas, debe especificar un cliente."
            )

        return data
=======
        if data['tipo'] == 'entrada' and not data.get('id_proveedor'):
            raise serializers.ValidationError("Para entradas, debe especificar un proveedor.")
        if data['tipo'] == 'salida' and not data.get('id_cliente'):
            raise serializers.ValidationError("Para salidas, debe especificar un cliente.")
        return data
>>>>>>> upstream/grupo5
