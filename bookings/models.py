# bookings/models.py
from django.db import models
from django.conf import settings
from datetime import timedelta
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

from pytz import all_timezones 

TIMEZONES = tuple(zip(all_timezones, all_timezones))

class ServiceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    base_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cost_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ServiceInstance(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name} ({self.service_type.name})'

class Discount(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)]
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.description} ({self.discount_percentage}%)'

class Booking(models.Model):
    STATUS_ACTIVE = 'ACTIVE'
    STATUS_CANCELED = 'CANCELED'
    STATUS_COMPLETED = 'COMPLETED'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Activa'),
        (STATUS_CANCELED, 'Cancelada'),
        (STATUS_COMPLETED, 'Completada'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service_instance = models.ForeignKey(ServiceInstance, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_hours = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    discount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    class Meta:
        ordering = ['start_time']

    def save(self, *args, **kwargs):

        duration: timedelta = self.end_time - self.start_time
        self.duration_hours = Decimal(duration.total_seconds() / 3600).quantize(Decimal('0.01'))

        service_type = self.service_instance.service_type
        base_cost = service_type.base_cost
        cost_per_hour = service_type.cost_per_hour
        
        self.cost = Decimal(base_cost + (cost_per_hour * self.duration_hours)).quantize(Decimal('0.01'))

        try:
            active_discount = self.service_instance.service_type.discount_set.get(is_active=True)
            discount_percentage = active_discount.discount_percentage / 100
            discount_amount = self.cost * discount_percentage
            self.discount = Decimal(discount_amount).quantize(Decimal('0.01'))
        except Discount.DoesNotExist:
            self.discount = Decimal('0.00')

        # 4. Calcular el costo final
        self.final_cost = (self.cost - self.discount).quantize(Decimal('0.01'))

        super().save(*args, **kwargs)

    def mark_completed_if_past(self, reference_time):
        if self.status == self.STATUS_ACTIVE and self.end_time <= reference_time:
            self.status = self.STATUS_COMPLETED
            self.save(update_fields=['status'])

    def __str__(self):
        return f'Reserva de {self.service_instance.name} por {self.user.username}'

class GlobalSettings(models.Model):
    """
    Modelo Singleton para almacenar la configuración global de reservas.
    """
    operating_start_time = models.TimeField(
        default='09:00:00',
        verbose_name="Hora de Apertura"
    )

    operating_end_time = models.TimeField(
        default='18:00:00',
        verbose_name="Hora de Cierre"
    )

    slot_duration_minutes = models.IntegerField(
        default=30,
        validators=[MinValueValidator(30)],
        verbose_name="Duración del Slot (minutos)"
    )

    system_time_zone = models.CharField(
        max_length=50,
        choices=TIMEZONES,
        default='America/New_York', # O cualquier TZ de tu preferencia.
        verbose_name="Zona Horaria del Sistema"
    )

    class Meta:
        verbose_name = "Configuración Global de Reserva"
        verbose_name_plural = "Configuración Global de Reservas"

    def save(self, *args, **kwargs):
        if not self.pk and GlobalSettings.objects.exists():
            raise Exception("Solo se permite una instancia de GlobalSettings.")
        return super(GlobalSettings, self).save(*args, **kwargs)
        
    @classmethod
    def load(cls):
        """Carga la única instancia, o crea una si no existe."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Configuración Global del Sistema"
