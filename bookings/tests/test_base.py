# bookings/tests/test_base.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from unittest.mock import patch, MagicMock

from users.models import CustomUser # Asumiendo la importación de tu modelo

# Mock de notifiers y reports
# Usaremos un path genérico, ajústalo si es necesario
NOTIFIER_CONFIRM_PATH = 'bookings.api.booking.BookingConfirmationNotifier'
NOTIFIER_CANCEL_PATH = 'bookings.api.booking.BookingCancellationNotifier'
REPORTS_PDF_PATH = 'bookings.api.booking.generate_pdf_report'
REPORTS_JSON_PATH = 'bookings.api.booking.generate_json_report'


class BaseAPITestCase(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        # 1. Crear usuarios con diferentes roles
        cls.client_user = CustomUser.objects.create_user(
            username='cliente_test', email='client@test.com', password='password123', role='CLIENT'
        )
        cls.staff_user = CustomUser.objects.create_user(
            username='staff_test', email='staff@test.com', password='password123', role='STAFF', is_staff=True
        )
        cls.admin_user = CustomUser.objects.create_superuser(
            username='admin_test', email='admin@test.com', password='password123', role='ADMIN'
        )
        cls.unauthenticated_user = None

    def setUp(self):
        self.client.logout()

    def force_authenticate(self, user):
        """Autentica el cliente de prueba con el usuario dado."""
        self.client.force_authenticate(user=user)

    def assertPermissionDenied(self, response):
        """Verifica que la respuesta sea un error de permiso denegado."""
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def assertNotAuthenticated(self, response):
        """Verifica que la respuesta sea un error de no autenticado."""
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)