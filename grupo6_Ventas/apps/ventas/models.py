from django.db import models

# Create your models here.
class Productos(models.Model):
    class meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
    nombre = models.CharField("Nombre",max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    
    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    class meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
    nombre = models.CharField("Nombre",max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    productos = models.ForeignKey(Productos, on_delete=models.CASCADE,null=True, blank=True) 
    

    def __str__(self):
        return f"{self.nombre}- {self.productos}"
