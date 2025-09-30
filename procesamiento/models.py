from django.db import models

class ProductoNegado(models.Model):
    fecha = models.DateField()
    producto = models.TextField()
    marca = models.CharField(max_length=100)
    cantidad_negada = models.DecimalField(max_digits=10, decimal_places=2)
    origen = models.CharField(max_length=100, null=True, blank=True)
    referencia = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.origen} - {self.marca} ({self.fecha})"
