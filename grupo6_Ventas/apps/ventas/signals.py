from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Venta

@receiver(post_save, sender=Venta)
def enviar_factura(sender, instance: Venta, created, **kwargs):
    if not created:
        return
    asunto = f"Factura Venta #{instance.id}"
    cuerpo = f"Hola {instance.cliente.nombre}, gracias por su compra. Total: {instance.total}"
    send_mail(asunto, cuerpo, None, [instance.cliente.email], fail_silently=True)
