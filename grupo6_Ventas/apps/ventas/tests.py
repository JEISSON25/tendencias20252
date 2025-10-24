from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase
from rest_framework import status
from apps.ventas.models import Productos, Cliente


class TestVentaFlow(APITestCase):
    """Flujo completo de ventas con autenticación JWT"""

    def setUp(self):
        # grupos
        vendedor_group, _ = Group.objects.get_or_create(name='vendedor')
        cliente_group, _ = Group.objects.get_or_create(name='cliente')

        # usuario vendedor
        self.vendedor = User.objects.create_user(
            username="vend", password="123456", email="vend@a.com"
        )
        self.vendedor.groups.add(vendedor_group)

        # datos base
        self.cliente = Cliente.objects.create(nombre="Juan", email="juan@a.com", telefono="123")
        self.prod = Productos.objects.create(nombre="Mouse", descripcion="Óptico", precio=50, stock=10)

        # token JWT
        resp = self.client.post("/api/token/", {"username": "vend", "password": "123456"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK, msg=resp.content)
        self.access = resp.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access}")

    def test_crear_venta(self):
        """Debe crear una venta correctamente"""
        payload = {
            "cliente": self.cliente.id,
            "detalles": [{"producto": self.prod.id, "cantidad": 2, "precio_unitario": "50.00"}]
        }
        resp = self.client.post("/api/ventas/", payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, msg=resp.content)
        self.assertEqual(float(resp.data["total"]), 100.0)

    def test_crear_venta_sin_token(self):
        """Debe rechazar si no se envía token"""
        self.client.credentials()  # quita el token
        payload = {
            "cliente": self.cliente.id,
            "detalles": [{"producto": self.prod.id, "cantidad": 1, "precio_unitario": "50.00"}]
        }
        resp = self.client.post("/api/ventas/", payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_crear_cliente(self):
        """Debe crear un nuevo cliente"""
        payload = {"nombre": "Ana", "email": "ana@a.com", "telefono": "321"}
        resp = self.client.post("/api/clientes/", payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, msg=resp.content)
        self.assertEqual(resp.data["nombre"], "Ana")

    def test_listar_clientes(self):
        """Debe listar al menos un cliente"""
        resp = self.client.get("/api/clientes/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) >= 1)

    def test_crear_producto(self):
        """Debe crear un nuevo producto"""
        payload = {"nombre": "Teclado", "descripcion": "Mecánico", "precio": 120, "stock": 3}
        resp = self.client.post("/api/productos/", payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["nombre"], "Teclado")

    def test_actualizar_producto(self):
        """Debe actualizar un producto existente"""
        payload = {"nombre": "Mouse Gamer", "descripcion": "RGB", "precio": 80, "stock": 5}
        resp = self.client.put(f"/api/productos/{self.prod.id}/", payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["nombre"], "Mouse Gamer")

    def test_eliminar_producto(self):
        """Debe eliminar un producto correctamente"""
        nuevo = Productos.objects.create(nombre="Eliminar", descripcion="x", precio=10, stock=1)
        resp = self.client.delete(f"/api/productos/{nuevo.id}/")
        self.assertIn(resp.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])

    def test_reporte_json(self):
        """Debe devolver reporte de ventas en formato JSON"""
        # crear una venta previa
        self.client.post("/api/ventas/", {
            "cliente": self.cliente.id,
            "detalles": [{"producto": self.prod.id, "cantidad": 1, "precio_unitario": "50.00"}]
        }, format="json")
        # obtener reporte
        resp = self.client.get("/api/reportes/ventas?format=json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("results", resp.data)

    #def test_reporte_pdf(self):
        """Debe devolver reporte de ventas en formato PDF"""
        # crear una venta previa
        #self.client.post("/api/ventas/", {
         #   "cliente": self.cliente.id,
            #"detalles": [{"producto": self.prod.id, "cantidad": 1, "precio_unitario": "50.00"}]
        #}, format="json")
        # obtener reporte PDF
       # resp = self.client.get("/api/reportes/ventas?format=pdf")
       #self.assertEqual(resp.status_code, status.HTTP_200_OK)
        #self.assertEqual(resp["Content-Type"], "application/pdf")
