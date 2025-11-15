from django.db import models
from django.conf import settings


class Log(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('error', 'Error'),
        ('warning', 'Warning'),
    ]

    LEVEL_CHOICES = [
        ('usuarios', 'Usuarios'),
        ('roles', 'Roles'),
        ('recursos', 'Recursos'),
        ('reservas', 'Reservas'),
        ('sistema', 'Sistema'),
        ('otro', 'Otro'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    message = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True, db_index=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='logs'
    )

    def __str__(self):
        user = self.usuario.username if self.usuario else 'system'
        return f"[{self.get_status_display()}] {self.get_level_display()} - {user} - {self.fecha_hora:%Y-%m-%d %H:%M:%S}"
