from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('CLIENT', 'Cliente Final'),
        ('STAFF', 'Personal de Servicio'),
        ('MANAGER', 'Gerente'),
        ('ADMIN', 'Administrador'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='CLIENT',
    )
    
    @property
    def is_client(self):
        return self.role == 'CLIENT'

    @property
    def is_manager_or_higher(self):
        return self.role in ('MANAGER', 'ADMIN')
    
    pass


class UserActivity(models.Model):
    """
    Store a trail of actions performed by authenticated users across the platform.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=512)
    status_code = models.PositiveIntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    query_params = models.TextField(blank=True)
    payload = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user} {self.method} {self.path} [{self.status_code}]'
