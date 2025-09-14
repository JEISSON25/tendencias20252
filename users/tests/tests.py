from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from ..models import CustomUser

class UserAuthenticationTests(APITestCase):

    def test_user_registration(self):
        url = reverse('register')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_user_login(self):
        CustomUser.objects.create_user(username='testuser', password='testpassword123')
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)