# bookings/tests/test_discount.py
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from bookings.models import Discount, ServiceType
from bookings.tests.test_base import BaseAPITestCase

class DiscountTests(BaseAPITestCase):
    
    def setUp(self):
        super().setUp()
        self.list_url = reverse('discount-list')
        
        self.service_type = ServiceType.objects.create(name='Service')
        self.discount = Discount.objects.create(
            service_type=self.service_type,
            description='Descuento de prueba',
            discount_percentage=Decimal('10.00')
        )
        self.valid_payload = {
            'service_type': self.service_type.pk,
            'description': 'Descuento Nuevo',
            'discount_percentage': '5.00',
            'is_active': True
        }

    # --- Permisos (STAFF_PERMISSIONS para todo) ---

    def test_permission_staff_can_create(self):
        self.force_authenticate(self.staff_user)
        response = self.client.post(self.list_url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_permission_client_cannot_list(self):
        self.force_authenticate(self.client_user)
        response = self.client.get(self.list_url)
        self.assertPermissionDenied(response)

    def test_permission_unauthenticated_cannot_delete(self):
        detail_url = reverse('discount-detail', args=[self.discount.pk])
        response = self.client.delete(detail_url)
        self.assertNotAuthenticated(response)