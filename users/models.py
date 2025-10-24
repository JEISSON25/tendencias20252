from django.db import models
from django.contrib.auth.models import AbstractUser

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