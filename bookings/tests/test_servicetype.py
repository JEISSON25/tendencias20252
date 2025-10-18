# bookings/tests/test_servicetype.py
from datetime import datetime
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from bookings.models import ServiceType
from bookings.tests.test_base import BaseAPITestCase, NOTIFIER_CONFIRM_PATH

class ServiceTypeTests(BaseAPITestCase):
    
    def setUp(self):
        super().setUp()
        self.list_url = reverse('servicetype-list')
        self.detail_url = lambda pk: reverse('servicetype-detail', args=[pk])
        
        self.service_type = ServiceType.objects.create(
            name='Sala de Reuniones',
            base_cost=Decimal('50.00'),
            cost_per_hour=Decimal('10.00')
        )
        self.valid_payload = {
            'name': 'Consultorio Médico',
            'description': 'Espacio para consultas',
            'base_cost': '100.00',
            'cost_per_hour': '25.00',
        }

    # --- Permisos (STAFF_PERMISSIONS) ---

    def test_permission_staff_can_list(self):
        self.force_authenticate(self.staff_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_client_cannot_list(self):
        self.force_authenticate(self.client_user)
        response = self.client.get(self.list_url)
        self.assertPermissionDenied(response)

    def test_permission_unauthenticated_cannot_create(self):
        response = self.client.post(self.list_url, self.valid_payload)
        self.assertNotAuthenticated(response)
    
    def test_permission_staff_can_create(self):
        self.force_authenticate(self.staff_user)
        response = self.client.post(self.list_url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceType.objects.count(), 2)

    # --- Funcionalidad CRUD ---

    def test_staff_can_update_servicetype(self):
        self.force_authenticate(self.staff_user)
        update_data = {'name': 'Sala VIP Actualizada'}
        response = self.client.patch(self.detail_url(self.service_type.pk), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.service_type.refresh_from_db()
        self.assertEqual(self.service_type.name, 'Sala VIP Actualizada')

    def test_staff_can_delete_servicetype(self):
        self.force_authenticate(self.staff_user)
        response = self.client.delete(self.detail_url(self.service_type.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ServiceType.objects.count(), 0)