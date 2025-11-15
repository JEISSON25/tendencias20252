from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class Usuarios (AbstractUser):
    rol = models.ForeignKey(
        "roles.Roles",
        on_delete=models.SET_NULL,
        null=True,
        related_name="usuarios"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.email}  - {self.rol} - {self.fecha_creacion}"
