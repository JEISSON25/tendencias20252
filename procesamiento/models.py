from django.db import models

class ProductoNegado(models.Model):
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)
    cantidad_real = models.IntegerField()
    cantidad_reservada = models.IntegerField()
    producto_negado = models.IntegerField()
    marca = models.CharField(max_length=100)
    documento_origen = models.CharField(max_length=100, null=True, blank=True)
    referencia = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.descripcion} - {self.marca} ({self.fecha})"
