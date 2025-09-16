from django.db import models

class Origen(models.Model):
    origen= models.CharField(max_length=10, unique=True)
    
    def __str__(self):
         return f"{self.origen}"


class Productos(models.Model):
    producto_referencia= models.CharField(max_length=10, unique=True) 
    producto_nombre = models.TextField()
    marca= models.CharField(max_length=40) 
    precio_ponderado = models.DecimalField(max_digits=10, decimal_places=2)
    peso_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
         return f"{self.producto_nombre} - {self.marca}"

class Lista_productos_negados(models.Model):
    producto_referencia=models.ForeignKey(Productos, on_delete=models.CASCADE)
    origen = models.ForeignKey(Origen, on_delete=models.CASCADE)
    cantidad_negada = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
         return f"{self.origen}"

class Lista_productos_pedidos(models.Model):
    producto_referencia=models.ForeignKey(Productos, on_delete=models.CASCADE)
    origen = models.ForeignKey(Origen, on_delete=models.CASCADE)
    cantidad_pedida = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
         return f"{self.origen}"
     
class Cuidad(models.Model):
    cuidad= models.TextField() 
    
    def __str__(self):
         return f"{self.cuidad}"
     
class Zona(models.Model):
    zona= models.TextField() 
    
    def __str__(self):
         return f"{self.zona}"
     
class Asociado(models.Model):
    cedula_Asociado=models.CharField(max_length=12) 
    nombre_Asociado=models.TextField() 
    cuidad = models.ForeignKey(Cuidad, on_delete=models.CASCADE)
    Zona = models.ForeignKey(Zona, on_delete=models.CASCADE)

    def __str__(self):
         return f"{self.nombre_Asociado} - {self.cedula_Asociado}"
     
class Vendedor(models.Model):
    vendedor= models.TextField() 
    
    def __str__(self):
         return f"{self.vendedor}"

class Conductor(models.Model):
    conductor= models.TextField() 
    
    def __str__(self):
         return f"{self.conductor}"
     
class Facturas_contabilidad(models.Model):
    origen = models.ForeignKey(Origen, on_delete=models.CASCADE) 
    fecha_factura = models.DateField()
    cedula_Asociado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    peso_total = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    id_importacion = models.TextField()
    estado_orden = models.BooleanField()
    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE)
    fecha_procesamiento = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
         return f"{self.origen}"


