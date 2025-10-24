from bookings.services.notifications.email_service import EmailApiService
from .utils import render_email_template
from bookings.models import Booking

class BookingConfirmationNotifier:
    def __init__(self):
        self.email_service = EmailApiService()

    def send_notification(self, booking: Booking):
        print(booking.user.email)
        recipient_email = booking.user.email
        subject = '✅ Confirmación de Reserva Exitosa'
        
        # Prepara el contexto para la plantilla
        context = {
            'username': booking.user,
            'service_instance_name': booking.service_instance.name,
            'start_time': booking.start_time,
            'end_time': booking.end_time,
            'final_cost': booking.final_cost,
            'site_name': 'Reservas Inteligentes',
        }
        
        # Renderiza el contenido de la plantilla
        # Asumiendo que tu plantilla es HTML: emails/booking_confirmation.html
        html_content = render_email_template('booking_confirmation.html', context)
        
        # Envía el correo
        self.email_service.send_email(
            recipient_email=recipient_email,
            subject=subject,
            html_content=html_content
        )