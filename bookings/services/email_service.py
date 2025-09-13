from django.core.mail import send_mail
from django.conf import settings
from django.template import loader

class EmailService:
    @staticmethod
    def send_booking_confirmation_email(booking):
        """
        Envía un correo de confirmación de reserva usando un template.
        """
        template = loader.get_template('bookings/templates/email/booking_cancellation.txt')
        context = {
            'username': booking.user.username,
            'service_instance_name': booking.service_instance.name,
            'start_time': booking.start_time,
            'end_time': booking.end_time,
            'final_cost': booking.final_cost,
            'site_name': 'Reservas Inteligentes',
        }
        message = template.render(context)
        
        subject = 'Confirmación de reserva'
        from_email = settings.EMAIL_HOST_USER
        user_email = booking.user.email

        try:
            send_mail(subject, message, from_email, [user_email])
            print(f"Correo de confirmación enviado a {user_email}")
        except Exception as e:
            print(f"Error al enviar correo de confirmación: {e}")

    @staticmethod
    def send_booking_cancellation_email(booking):
        """
        Envía un correo de cancelación de reserva usando un template.
        """
        template = loader.get_template('bookings/templates/email/booking_cancellation.txt')
        context = {
            'username': booking.user.username,
            'service_instance_name': booking.service_instance.name,
            'start_time': booking.start_time,
            'end_time': booking.end_time,
            'site_name': 'Reservas Inteligentes',
        }
        message = template.render(context)
        
        subject = 'Cancelación de reserva'
        from_email = settings.EMAIL_HOST_USER
        user_email = booking.user.email

        try:
            send_mail(subject, message, from_email, [user_email])
            print(f"Correo de cancelación enviado a {user_email}")
        except Exception as e:
            print(f"Error al enviar correo de cancelación: {e}")