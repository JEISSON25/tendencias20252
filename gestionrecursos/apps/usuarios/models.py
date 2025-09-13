from django.db import models

# Create your models here.
class Usuarios(models.Model):
    id_usuario = models.CharField("Cedula del Usuario", max_length=20, primary_key = True)
    nombre_usuario = models.CharField("Nombre del usuario", max_length=50)
    email_usuario = models.CharField("Email del usuario", max_length=50)
    contrasena = models.CharField("Contraseña del usuario", max_length=15)
    id_rol = models.ForeignKey(
        "roles.Roles",
        on_delete=models.SET_NULL,
        null=True,
        related_name="usuarios"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_usuario} - {self.nombre_usuario} - {self.email_usuario} - {self.contrasena} - {self.id_rol} - {self.fecha_creacion}"
