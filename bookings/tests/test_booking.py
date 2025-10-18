# bookings/tests/test_booking.py
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from requests import Response
from rest_framework import status
from decimal import Decimal
from bookings.models import Booking, ServiceInstance, ServiceType, Discount
from bookings.tests.test_base import BaseAPITestCase, NOTIFIER_CONFIRM_PATH, NOTIFIER_CANCEL_PATH, REPORTS_PDF_PATH, REPORTS_JSON_PATH
from unittest.mock import patch

class BookingTests(BaseAPITestCase):
    
    def setUp(self):
        super().setUp()
        self.list_url = reverse('booking-list')
        
        self.service_type = ServiceType.objects.create(
            name='Habitación', base_cost=Decimal('50.00'), cost_per_hour=Decimal('10.00')
        )
        self.instance = ServiceInstance.objects.create(
            service_type=self.service_type, name='Habitación Individual'
        )

        now = timezone.now()
        
        # Booking del cliente (propia)
        self.client_booking = Booking.objects.create(
            user=self.client_user,
            service_instance=self.instance,
            start_time=now + timedelta(hours=1),
            end_time=now + timedelta(hours=2)
        )
        # Booking de otro usuario (para pruebas de queryset/permisos de objeto)
        self.admin_booking = Booking.objects.create(
            user=self.admin_user,
            service_instance=self.instance,
            start_time=now + timedelta(hours=3),
            end_time=now + timedelta(hours=4)
        )
        
        self.valid_payload = {
            'service_instance': self.instance.pk,
            'start_time': (now + timedelta(hours=5)).isoformat(),
            'end_time': (now + timedelta(hours=6)).isoformat(),
        }

    # --- Permisos BookingViewSet ---

    def test_client_can_list_only_their_bookings(self):
        self.force_authenticate(self.client_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Debe ver solo su reserva, no la del admin
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.client_booking.pk)

    def test_staff_can_list_all_bookings(self):
        self.force_authenticate(self.staff_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Debe ver todas las reservas
        self.assertEqual(len(response.data), 2)
        
    def test_client_cannot_update_booking(self):
        now = timezone.now()

        self.force_authenticate(self.client_user)
        
        update_data = {'start_time': (now + timedelta(hours=10)).isoformat()}
        
        detail_url = reverse('booking-detail', args=[self.client_booking.pk])
        
        response = self.client.patch(detail_url, update_data, format='json')
        # Falla porque requiere STAFF_PERMISSIONS para update
        self.assertPermissionDenied(response) 

    # El cliente sí puede CANCELAR su propia reserva (destroy)
    @patch(NOTIFIER_CANCEL_PATH)
    def test_client_can_delete_their_booking(self, mock_notifier):
        self.force_authenticate(self.client_user)
        detail_url = reverse('booking-detail', args=[self.client_booking.pk])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 1)
        mock_notifier.return_value.send_notification.assert_called_once()
    
    # --- Funcionalidad BookingViewSet ---

    @patch(NOTIFIER_CONFIRM_PATH)
    def test_create_sends_confirmation_and_saves_calculations(self, mock_notifier):
        self.force_authenticate(self.client_user)
        response = self.client.post(self.list_url, self.valid_payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_booking = Booking.objects.get(pk=response.data['id'])
        
        # Verifica la notificación
        mock_notifier.return_value.send_notification.assert_called_once()
        
        # Verifica los cálculos del modelo (1 hora * 10.00/hr + 50.00 base = 60.00)
        self.assertEqual(new_booking.duration_hours, Decimal('1.00'))
        self.assertEqual(new_booking.cost, Decimal('60.00'))
        self.assertEqual(new_booking.final_cost, Decimal('60.00'))

# --- Pruebas BookingReportViewSet ---

class BookingReportTests(BaseAPITestCase):

    def setUp(self):
        super().setUp()
        self.pdf_url = reverse('report_pdf')
        self.json_url = reverse('report_json')
        
        now = timezone.now()

        # Crear datos de prueba para los reportes
        service_type = ServiceType.objects.create(name='T')
        instance = ServiceInstance.objects.create(service_type=service_type, name='I')
        Booking.objects.create(
            user=self.client_user, service_instance=instance, 
            start_time=now, end_time=now + timedelta(hours=1)
        )

    # --- Permisos (STAFF_PERMISSIONS para reportes) ---

    def test_permission_client_cannot_access_reports(self):
        self.force_authenticate(self.client_user)
        response = self.client.get(self.pdf_url)
        self.assertPermissionDenied(response)
    
    def test_permission_staff_can_access_pdf_report(self):
        self.force_authenticate(self.staff_user)
        # Mock para evitar errores de renderizado/librerías externas en la prueba
        with patch(REPORTS_PDF_PATH) as mock_pdf:
            mock_pdf.return_value = Response("Mock PDF Content", status=status.HTTP_200_OK)
            response = self.client.get(self.pdf_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            mock_pdf.assert_called_once()

    def test_permission_staff_can_access_json_report(self):
        self.force_authenticate(self.staff_user)
        with patch(REPORTS_JSON_PATH) as mock_json:
            mock_json.return_value = Response({"data": "Mock JSON"}, status=status.HTTP_200_OK)
            response = self.client.get(self.json_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            mock_json.assert_called_once()