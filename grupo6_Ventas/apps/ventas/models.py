from django.conf import settings
from django.db import models

class Productos(models.Model):
    nombre = models.CharField("Nombre", max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField("Nombre", max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    def __str__(self):
        return f"{self.nombre}"

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="ventas")
    vendedor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="ventas_realizadas")
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    def __str__(self):
        return f"Venta #{self.id} - {self.cliente} - {self.fecha:%Y-%m-%d}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Productos, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    def __str__(self):
        return f"{self.producto} x {self.cantidad} @ {self.precio_unitario}"