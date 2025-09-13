from django.db import models

class Categoria(models.Model):
   
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    
    nombre = models.CharField(max_length=150)
    contacto = models.CharField(max_length=100,unique=True )

    def __str__(self):
        return self.nombre

class Producto(models.Model):
   
    nombre = models.CharField(max_length=150)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="productos")
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="productos_proveedor")

    def __str__(self):
        return f"{self.nombre} ({self.id_categoria})"

class Cliente(models.Model):
    
    nombre = models.CharField(max_length=150)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
   
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    cargo = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class FacturaVenta(models.Model):
    
    fecha = models.DateField(auto_now_add=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="facturas")
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name="facturas")

    def __str__(self):
        return f"Factura {self.id}"

class DetalleVenta(models.Model):
    
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    id_factura = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE, related_name="detalles")
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="detalles")

    def __str__(self):
        return f"Detalle {self.id} (Factura {self.id_factura})"

class Movimiento(models.Model):
    TIPOS_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

  
    tipo = models.CharField(max_length=10, choices=TIPOS_MOVIMIENTO)
    cantidad = models.IntegerField(default=1)
    fecha = models.DateField(auto_now_add=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="movimientos")
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="movimientos", blank=True, null=True)

    def __str__(self):
        return f"Movimiento {self.id} ({self.tipo})"
