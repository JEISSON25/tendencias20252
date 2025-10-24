# bookings/tests/test_serviceinstance.py
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from bookings.models import ServiceInstance, ServiceType
from bookings.tests.test_base import BaseAPITestCase

class ServiceInstanceTests(BaseAPITestCase):
    
    def setUp(self):
        super().setUp()
        self.list_url = reverse('service-instance-list')
        
        self.service_type = ServiceType.objects.create(
            name='Office', base_cost=Decimal('10.00'), cost_per_hour=Decimal('5.00')
        )
        self.instance = ServiceInstance.objects.create(
            service_type=self.service_type, name='Oficina 101'
        )
        self.valid_payload = {
            'service_type': self.service_type.pk,
            'name': 'Oficina 102',
            'description': 'Una nueva oficina',
        }

    # --- Permisos (AUTH para Read, STAFF para Write) ---

    def test_permission_client_can_list(self):
        self.force_authenticate(self.client_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_staff_can_create(self):
        self.force_authenticate(self.staff_user)
        response = self.client.post(self.list_url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceInstance.objects.count(), 2)
    
    def test_permission_client_cannot_create(self):
        self.force_authenticate(self.client_user)
        response = self.client.post(self.list_url, self.valid_payload)
        self.assertPermissionDenied(response) # Falla porque requiere STAFF

    def test_permission_unauthenticated_cannot_list(self):
        response = self.client.get(self.list_url)
        self.assertNotAuthenticated(response)