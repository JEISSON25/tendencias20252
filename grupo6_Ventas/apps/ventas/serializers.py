from rest_framework import serializers
from .models import Productos, Cliente, Venta, DetalleVenta

class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = '__all__'



class DetalleVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source="producto.nombre")
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = DetalleVenta
        fields = ['id','producto','producto_nombre','cantidad','precio_unitario','subtotal']

    def get_subtotal(self, obj):
        return float(obj.cantidad) * float(obj.precio_unitario)

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)
    cliente_nombre = serializers.ReadOnlyField(source="cliente.nombre")
    vendedor_username = serializers.ReadOnlyField(source="vendedor.username")

    class Meta:
        model = Venta
        fields = ['id','cliente','cliente_nombre','vendedor','vendedor_username','fecha','total','detalles']
        read_only_fields = ['fecha','total','vendedor']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['vendedor'] = request.user
        venta = Venta.objects.create(**validated_data)
        total = 0
        for d in detalles_data:
            detalle = DetalleVenta.objects.create(venta=venta, **d)
            total += detalle.cantidad * detalle.precio_unitario
        venta.total = total
        venta.save()
        return venta

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if detalles_data is not None:
            instance.detalles.all().delete()
            total = 0
            for d in detalles_data:
                detalle = DetalleVenta.objects.create(venta=instance, **d)
                total += detalle.cantidad * detalle.precio_unitario
            instance.total = total
        instance.save()
        return instance
