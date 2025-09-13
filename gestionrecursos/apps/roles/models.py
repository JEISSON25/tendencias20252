from django.db import models

# Create your models here.
class Roles(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField("Nombre del rol", max_length=50)
    descripcion_rol = models.CharField("Descripcion", max_length=150, null=True)

    def __str__(self):
        return f"{self.id_rol} - {self.nombre_rol} - {self.descripcion_rol}"
