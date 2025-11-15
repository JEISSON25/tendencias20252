from django.db import models
from django.contrib.auth.models import AbstractUser



# Modelo de Usuario Personalizado 
class CustomUser(AbstractUser):
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.email or self.username


class MovimientoUsuario(models.Model):
    
    usuario = models.ForeignKey(
        'users.CustomUser', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Usuario Activo"
    )

    fecha_actividad = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha y Hora"
    )
    actividad = models.CharField(max_length=255, verbose_name="Actividad Realizada")
    detalle = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Movimiento de Usuario"
        ordering = ['-fecha_actividad']