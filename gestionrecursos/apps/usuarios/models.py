from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class Usuarios (AbstractUser):
    
    nombre_usuario = models.CharField("Nombre del usuario", max_length=50)
    email_usuario = models.CharField("Email del usuario", max_length=50)
    rol = models.ForeignKey(
        "roles.Roles",
        on_delete=models.SET_NULL,
        null=True,
        related_name="usuarios"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.nombre_usuario} - {self.email_usuario}  - {self.rol} - {self.fecha_creacion}"
