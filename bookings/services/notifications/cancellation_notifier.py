from bookings.services.notifications.email_service import EmailApiService
from .utils import render_email_template
from bookings.models import Booking

class BookingCancellationNotifier:
    def __init__(self):
        self.email_service = EmailApiService()

    def send_notification(self, booking: Booking):
        recipient_email = booking.user.email
        subject = '❌ Cancelación de Reserva'
        
        context = {
            'username': booking.user.username,
            'service_instance_name': booking.service_instance.name,
            'start_time': booking.start_time,
            'end_time': booking.end_time,
            'site_name': 'Reservas Inteligentes',
        }
        
        html_content = render_email_template('booking_cancellation.html', context)
        
        self.email_service.send_email(
            recipient_email=recipient_email,
            subject=subject,
            html_content=html_content
        )