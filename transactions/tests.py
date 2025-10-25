<<<<<<< HEAD
from django.test import TestCase

# Create your tests here.
=======
from decimal import Decimal

from django.contrib.auth.models import User
# Create your tests here.

from django.test import TestCase, Client
from rest_framework import status

import clients.models
from products.models import Product
from transactions.models import Transaction


# Create your tests here.

class ClientTestCase(TestCase):
    def setUp(self):
        User.objects.create_superuser('test', 'test@gmail.com', 'testpass')
        self.client = Client()
        token = self.client.post("/api/auth/login/", {"username": "test", "password": "testpass"}).json()["token"]
        self.client = Client(headers={"authorization": token})

    def test_create_transaction_successfully(self):
        Product.objects.create(
            name="Another Product",
            category="Another Category",
            subcategory="Another Subcategory",
            price=25000.00,
            quantity=15
        )

        clients.models.Client.objects.create(
            document= "test",
            name="test",
            last_name="test",
            email="test@example.com",
            phone="123456789",
            address= "test #123-45"
        )

        transaction_request: dict[str, object] ={
          "client": "test",
          "products": [
            {
              "product": 1,
              "quantity": 2
            }
          ],
          "payment_method": "cash",
          "status": "PAGADO"
        }
        response = self.client.post("/api/transactions/", transaction_request, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), {
          "id": response.json()["id"],
          "payment_method": "cash",
          "status": "PAGADO",
          "total": "50000.00",
          "client": "test",
          "products": [1]
        })

    def test_get_transaction_by_id_successfully(self):
        Product.objects.create(
            name="Another Product",
            category="Another Category",
            subcategory="Another Subcategory",
            price=25000.00,
            quantity=15
        )

        clients.models.Client.objects.create(
            document= "test",
            name="test",
            last_name="test",
            email="test@example.com",
            phone="123456789",
            address= "test #123-45"
        )

        transaction = Transaction.objects.create(client=clients.models.Client(document="test"), total=Decimal(50000))

        response = self.client.get(f"/api/transactions/{transaction.id}/", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_transactions_successfully(self):
        Product.objects.create(
            name="Another Product",
            category="Another Category",
            subcategory="Another Subcategory",
            price=25000.00,
            quantity=15
        )

        clients.models.Client.objects.create(
            document= "test",
            name="test",
            last_name="test",
            email="test@example.com",
            phone="123456789",
            address= "test #123-45"
        )

        Transaction.objects.create(client=clients.models.Client(document="test"), total=Decimal(50000))
        Transaction.objects.create(client=clients.models.Client(document="test"), total=Decimal(60000))

        response = self.client.get("/api/transactions/", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_update_transaction_successfully(self):
        Product.objects.create(
            name="Another Product",
            category="Another Category",
            subcategory="Another Subcategory",
            price=25000.00,
            quantity=15
        )

        clients.models.Client.objects.create(
            document= "test",
            name="test",
            last_name="test",
            email="test@example.com",
            phone="123456789",
            address= "test #123-45"
        )
        transaction_request: dict[str, object] ={
          "client": "test",
          "products": [],
          "payment_method": "cash",
          "status": "PENDIENTE"
        }
        transaction1 = Transaction.objects.create(client=clients.models.Client(document="test"), total=Decimal(50000))
        transaction2 = Transaction.objects.create(client=clients.models.Client(document="test"), total=Decimal(60000))

        response = self.client.put(f"/api/transactions/{transaction2.id}/", transaction_request, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], "PENDIENTE")

    def test_delete_product_successfully(self):
        Product.objects.create(
            name="Another Product",
            category="Another Category",
            subcategory="Another Subcategory",
            price=25000.00,
            quantity=15
        )

        clients.models.Client.objects.create(
            document= "test",
            name="test",
            last_name="test",
            email="test@example.com",
            phone="123456789",
            address= "test #123-45"
        )

        transaction = Transaction.objects.create(client=clients.models.Client(document="test"), total=Decimal(50000))

        response = self.client.delete(f"/api/transactions/{transaction.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(id=transaction.id)
>>>>>>> repo2/main
