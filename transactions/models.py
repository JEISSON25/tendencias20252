import uuid
<<<<<<< HEAD
=======
from datetime import datetime
from decimal import Decimal
>>>>>>> repo2/main

from django.db import models

from clients.models import Client
from products.models import Product


# Create your models here.

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="ProductPerTransaction")
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def to_dict(self):
        return {
            "id": self.id,
            "client": self.client.document,
            'products': [product.to_dict() for product in ProductPerTransaction.objects.filter(transaction_id=self.id).all()],
            "payment_method": self.payment_method,
            "status": self.status,
            "total": self.total,
        }

class ProductPerTransaction(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def to_dict(self):
        return {
            "product": self.product.name,
            "quantity": self.quantity,
            "total": self.total,
<<<<<<< HEAD
=======
        }

class Report:
    def __init__(self, total_clients: int, total_products: int, num_sales: int, total_sales: Decimal,
                 best_selling_product: str, selling_by_products: dict[str, Decimal]):
        self.title = "Reporte de ventas"
        self.total_clients = total_clients
        self.total_products = total_products
        self.num_sales = num_sales
        self.total_sales = total_sales
        self.best_selling_product = best_selling_product
        self.selling_by_products = selling_by_products
        self.created_date = datetime.now()

    def to_dict(self):
        return {
            "title": self.title,
            "created_date": self.created_date,
            "total_clients": self.total_clients,
            "total_products": self.total_products,
            "num_sales": self.num_sales,
            "total_sales": self.total_sales,
            "best_selling_product": self.best_selling_product,
            "selling_by_products": self.selling_by_products,
>>>>>>> repo2/main
        }