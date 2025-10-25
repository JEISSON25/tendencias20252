<<<<<<< HEAD
from django.test import TestCase

# Create your tests here.
=======
from django.contrib.auth.models import User
# Create your tests here.

from django.test import TestCase, Client
from rest_framework import status

import clients.models

# Create your tests here.

class ClientTestCase(TestCase):
    def setUp(self):
        User.objects.create_superuser('test', 'test@gmail.com', 'testpass')
        self.client = Client()
        token = self.client.post("/api/auth/login/", {"username": "test", "password": "testpass"}).json()["token"]
        self.client = Client(headers={"authorization": token})

    def test_create_client_successfully(self):
        client_request: dict[str, object] = {
          "document": "test",
          "name": "test",
          "last_name": "test",
          "email": "test@example.com",
          "phone": "123456789",
          "address": "test #123-45"
        }
        response = self.client.post("/api/clients/", client_request, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), {
          "document": "test",
          "name": "test",
          "last_name": "test",
          "email": "test@example.com",
          "phone": "123456789",
          "address": "test #123-45"
        })

    def test_get_client_by_id_successfully(self):
        clients.models.Client.objects.create(
            document= "test",
            name="test",
            last_name="test",
            email="test@example.com",
            phone="123456789",
            address= "test #123-45"
        )

        response = self.client.get("/api/clients/test/", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), {
          "document": "test",
          "name": "test",
          "last_name": "test",
          "email": "test@example.com",
          "phone": "123456789",
          "address": "test #123-45"
        })

    def test_get_all_clients_successfully(self):
        clients.models.Client.objects.create(
            document= "test",
            name="test",
            last_name="test",
            email="test@example.com",
            phone="123456789",
            address= "test #123-45"
        )
        clients.models.Client.objects.create(
            document= "test2",
            name="test2",
            last_name="test2",
            email="test2@example.com",
            phone="123456789",
            address= "test #123-45"
        )

        response = self.client.get("/api/clients/", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.json(), [{
          "document": "test",
          "name": "test",
          "last_name": "test",
          "email": "test@example.com",
          "phone": "123456789",
          "address": "test #123-45"
        },
        {
          "document": "test2",
          "name": "test2",
          "last_name": "test2",
          "email": "test2@example.com",
          "phone": "123456789",
          "address": "test #123-45"
        }
        ])

    def test_update_product_successfully(self):
        clients.models.Client.objects.create(
            document= "test",
            name="test",
            last_name="test",
            email="test@example.com",
            phone="123456789",
            address= "test #123-45"
        )
        clients.models.Client.objects.create(
            document= "test2",
            name="test2",
            last_name="test2",
            email="test2@example.com",
            phone="123456789",
            address= "test #123-45"
        )
        client_request: dict[str, object] = {
          "document": "test2",
          "name": "test updated",
          "last_name": "test updated",
          "email": "test2@example.com",
          "phone": "123456789",
          "address": "test #123-45"
        }

        response = self.client.put("/api/clients/test2/", client_request, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(),
        {
            "document": "test2",
            "name": "test updated",
            "last_name": "test updated",
            "email": "test2@example.com",
            "phone": "123456789",
            "address": "test #123-45"
        })

    def test_delete_product_successfully(self):
        clients.models.Client.objects.create(
            document= "test",
            name="test",
            last_name="test",
            email="test@example.com",
            phone="123456789",
            address= "test #123-45"
        )

        response = self.client.delete("/api/clients/test/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(clients.models.Client.DoesNotExist):
            clients.models.Client.objects.get(document="test")
>>>>>>> repo2/main
