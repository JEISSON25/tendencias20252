from django.db import models


class CortesLogistico(models.Model):
    fecha = models.DateField()
    nombre = models.TextField(max_length=200, unique=True)
    def __str__(self):
        return f"{self.fecha} - {self.nombre}"
    

class ProductoNegado(models.Model):
    fecha = models.DateField()
    producto = models.CharField(max_length=200) 
    marca = models.CharField(max_length=100)
    cantidad_negada = models.DecimalField(max_digits=10, decimal_places=2)
    origen = models.CharField(max_length=7, null=False, blank=False)
    referencia = models.CharField(max_length=100, null=False, blank=False) 

    def __str__(self):
        return f"{self.origen} - {self.marca} ({self.fecha})"

class pickingModel(models.Model): 
    nombreAsociado = models.CharField(max_length=500) 
    fechaFactura = models.DateField()
    identificacionAsociado = models.CharField(max_length=15) 
    vendedor = models.CharField(max_length=100) 
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    producto = models.TextField(max_length=1000) 
    pesoUnitario = models.DecimalField(max_digits=10, decimal_places=2)
    cuidad = models.CharField(max_length=50) 
    codigoZona = models.CharField(max_length=50) 
    zona = models.CharField(max_length=50) 
    origen = models.CharField(max_length=7) 
    marca = models.CharField(max_length=50) 
    idOdoo= models.CharField(max_length=250) 
    fecha_procesamiento = models.DateField(auto_now_add=True)
    nombrecorte = models.ForeignKey(CortesLogistico, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.origen} - {self.zona} ({self.fechaFactura})" 