from django.db import models
from django.forms import ValidationError
from django.core.mail import send_mail
from django.conf import settings

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
    id_user =models.ForeignKey(
        "usuarios.Usuarios",
        on_delete=models.SET_NULL,
        null=True,
        related_name="reservas",
        blank=True
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
        return f"Reserva {self.id_reserva} - {self.estado_reserva} - {self.id_user.username} - {self.id_recurso.tipo_recurso} - {self.fecha_inicio} - {self.fecha_fin} "
        
    def clean(self):
        if self.fecha_inicio >= self.fecha_fin:
            raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")
    
        # Verificar si existe alguna reserva que cruce con las fechas de esta reserva 
        Reservation_crussade = Reservas.objects.filter(
            id_recurso=self.id_recurso,
            fecha_fin=self.fecha_fin, 
            fecha_inicio=self.fecha_inicio
        ).exclude(id_reserva=self.id_reserva)

        if Reservation_crussade.exists():
            raise ValidationError("Ya existe una reserva para este recurso.")
    
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        print(self.id_user.email)
        send_mail(
            f'Cambio de estado: {self.estado_reserva}',
            f'Hola {self.id_user.username},\nNotificacion del estado de tu reserva para: {self.id_recurso.tipo_recurso} desde {self.fecha_inicio} hasta {self.fecha_fin}.',
            settings.DEFAULT_FROM_EMAIL,
            [self.id_user.email],
            fail_silently=False,
        )
 