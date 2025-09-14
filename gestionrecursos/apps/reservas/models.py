from django.db import models

class Reservas(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    ESTADOS_RESERVA = [
        ("PENDIENTE", "Pendiente"),
        ("CONFIRMADA", "Confirmada"),
        ("CANCELADA", "Cancelada"),
        ("FINALIZADA", "Finalizada"),
    ]
    estado_reserva = models.CharField(
        "Estado de la reserva",
        max_length=10,
        choices=ESTADOS_RESERVA,
        default="PENDIENTE"
    )
    id_usuario =models.ForeignKey(
        "usuarios.Usuarios",
        on_delete=models.SET_NULL,
        null=True,
        related_name="reservas"
    )
    id_recurso = models.ForeignKey(
        "recursos.Recursos",
        on_delete=models.SET_NULL,
        null=True,
        related_name="reservas"
    )
    fecha_inicio = models.DateTimeField("Fecha y hora de inicio", null=True)
    fecha_fin = models.DateTimeField("Fecha y hora de fin",null=True)

    def __str__(self):
        return f"Reserva {self.id_reserva} - {self.estado_reserva} - {self.id_usuario} - {self.id_recurso} - {self.fecha_inicio} - {self.fecha_fin} "
