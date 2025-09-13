from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import (
    Categoria, Proveedor, Producto,
    Cliente, Empleado, FacturaVenta,
    DetalleVenta, Movimiento
)

class CategoriaTests(APITestCase):
    def setUp(self):
        self.categoria_data = {'nombre': 'Medicamentos'}
        self.categoria = Categoria.objects.create(nombre='Vitaminas')

    def test_crear_categoria(self):
        url = reverse('categoria-list')
        response = self.client.post(url, self.categoria_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Categoria.objects.count(), 2)

        # Usar latest('id') para obtener la última categoría creada
        ultima_categoria = Categoria.objects.latest('id')
        self.assertEqual(ultima_categoria.nombre, 'Medicamentos')

    def test_listar_categorias(self):
        url = reverse('categoria-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_obtener_categoria(self):
        url = reverse('categoria-detail', args=[self.categoria.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Vitaminas')

    def test_actualizar_categoria(self):
        url = reverse('categoria-detail', args=[self.categoria.id])
        updated_data = {'nombre': 'Suplementos'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nombre, 'Suplementos')

    def test_eliminar_categoria(self):
        url = reverse('categoria-detail', args=[self.categoria.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Categoria.objects.count(), 0)

class ProveedorTests(APITestCase):
    def setUp(self):
        self.proveedor_data = {'nombre': 'Proveedor Ejemplo', 'contacto': 'contacto@ejemplo.com'}
        self.proveedor = Proveedor.objects.create(nombre='Proveedor Inicial', contacto='inicial@ejemplo.com')

    def test_crear_proveedor(self):
        url = reverse('proveedor-list')
        response = self.client.post(url, self.proveedor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Proveedor.objects.count(), 2)

        # Usar latest('id') para obtener el último proveedor creado
        ultimo_proveedor = Proveedor.objects.latest('id')
        self.assertEqual(ultimo_proveedor.nombre, 'Proveedor Ejemplo')

    def test_listar_proveedores(self):
        url = reverse('proveedor-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_obtener_proveedor(self):
        url = reverse('proveedor-detail', args=[self.proveedor.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Proveedor Inicial')

    def test_actualizar_proveedor(self):
        url = reverse('proveedor-detail', args=[self.proveedor.id])
        updated_data = {'nombre': 'Proveedor Actualizado', 'contacto': 'actualizado@ejemplo.com'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.proveedor.refresh_from_db()
        self.assertEqual(self.proveedor.nombre, 'Proveedor Actualizado')

    def test_eliminar_proveedor(self):
        url = reverse('proveedor-detail', args=[self.proveedor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Proveedor.objects.count(), 0)

class ProductoTests(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Medicamentos')
        self.proveedor = Proveedor.objects.create(nombre='Proveedor Ejemplo', contacto='contacto@ejemplo.com')
        self.producto_data = {
            'nombre': 'Paracetamol',
            'precio': 10.50,
            'stock': 100,
            'id_categoria': self.categoria.id,
            'id_proveedor': self.proveedor.id
        }
        self.producto = Producto.objects.create(
            nombre='Ibuprofeno',
            precio=15.75,
            stock=50,
            id_categoria=self.categoria,
            id_proveedor=self.proveedor
        )

    def test_crear_producto(self):
        url = reverse('producto-list')
        response = self.client.post(url, self.producto_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 2)

        # Usar latest('id') para obtener el último producto creado
        ultimo_producto = Producto.objects.latest('id')
        self.assertEqual(ultimo_producto.nombre, 'Paracetamol')

    def test_listar_producto(self):
        url = reverse('producto-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_obtener_producto(self):
        url = reverse('producto-detail', args=[self.producto.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Ibuprofeno')

    def test_actualizar_producto(self):
        url = reverse('producto-detail', args=[self.producto.id])
        updated_data = {
            'nombre': 'Paracetamol 500mg',
            'precio': 12.50,
            'stock': 150,
            'id_categoria': self.categoria.id,
            'id_proveedor': self.proveedor.id
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, 'Paracetamol 500mg')

    def test_eliminar_producto(self):
        url = reverse('producto-detail', args=[self.producto.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Producto.objects.count(), 0)

class ClienteTests(APITestCase):
    def setUp(self):
        self.cliente_data = {'nombre': 'Juan Pérez', 'correo': 'juan@example.com', 'telefono': '3123456789'}
        self.cliente = Cliente.objects.create(nombre='Carlos López', correo='carlos@example.com', telefono='3101234567')

    def test_crear_cliente(self):
        url = reverse('cliente-list')
        response = self.client.post(url, self.cliente_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 2)

        # Usar latest('id') para obtener el último cliente creado
        ultimo_cliente = Cliente.objects.latest('id')
        self.assertEqual(ultimo_cliente.nombre, 'Juan Pérez')

    def test_listar_clientes(self):
        url = reverse('cliente-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_obtener_cliente(self):
        url = reverse('cliente-detail', args=[self.cliente.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Carlos López')

    def test_actualizar_cliente(self):
        url = reverse('cliente-detail', args=[self.cliente.id])
        updated_data = {'nombre': 'Carlos López Actualizado', 'correo': 'carlos.actualizado@example.com', 'telefono': '3101234567'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.nombre, 'Carlos López Actualizado')

    def test_eliminar_cliente(self):
        url = reverse('cliente-detail', args=[self.cliente.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Cliente.objects.count(), 0)

class EmpleadoTests(APITestCase):
    def setUp(self):
        self.empleado_data = {'nombre': 'Ana Gómez', 'telefono': '3134567890', 'cargo': 'Vendedora'}
        self.empleado = Empleado.objects.create(nombre='Luis Martínez', telefono='3145678901', cargo='Gerente')

    def test_crear_empleado(self):
        url = reverse('empleado-list')
        response = self.client.post(url, self.empleado_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Empleado.objects.count(), 2)

        # Usar latest('id') para obtener el último empleado creado
        ultimo_empleado = Empleado.objects.latest('id')
        self.assertEqual(ultimo_empleado.nombre, 'Ana Gómez')

    def test_listar_empleados(self):
        url = reverse('empleado-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_obtener_empleado(self):
        url = reverse('empleado-detail', args=[self.empleado.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Luis Martínez')

    def test_actualizar_empleado(self):
        url = reverse('empleado-detail', args=[self.empleado.id])
        updated_data = {'nombre': 'Luis Martínez Actualizado', 'telefono': '3145678901', 'cargo': 'Supervisor'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.empleado.refresh_from_db()
        self.assertEqual(self.empleado.cargo, 'Supervisor')

    def test_eliminar_empleado(self):
        url = reverse('empleado-detail', args=[self.empleado.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Empleado.objects.count(), 0)

class FacturaVentaTests(APITestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nombre='Carlos López', correo='carlos@example.com', telefono='3101234567')
        self.empleado = Empleado.objects.create(nombre='Luis Martínez', telefono='3145678901', cargo='Gerente')
        self.factura_data = {
            'id_cliente': self.cliente.id,
            'id_empleado': self.empleado.id
        }
        self.factura = FacturaVenta.objects.create(
            id_cliente=self.cliente,
            id_empleado=self.empleado
        )

    def test_crear_factura(self):
        url = reverse('facturaventa-list')
        response = self.client.post(url, self.factura_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FacturaVenta.objects.count(), 2)

    def test_listar_facturas(self):
        url = reverse('facturaventa-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_obtener_factura(self):
        url = reverse('facturaventa-detail', args=[self.factura.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_eliminar_factura(self):
        url = reverse('facturaventa-detail', args=[self.factura.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FacturaVenta.objects.count(), 0)

class DetalleVentaTests(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Medicamentos')
        self.proveedor = Proveedor.objects.create(nombre='Proveedor Ejemplo', contacto='contacto@ejemplo.com')
        self.producto = Producto.objects.create(
            nombre='Paracetamol',
            precio=10.50,
            stock=100,
            id_categoria=self.categoria,
            id_proveedor=self.proveedor
        )
        self.cliente = Cliente.objects.create(nombre='Carlos López', correo='carlos@example.com', telefono='3101234567')
        self.empleado = Empleado.objects.create(nombre='Luis Martínez', telefono='3145678901', cargo='Gerente')
        self.factura = FacturaVenta.objects.create(
            id_cliente=self.cliente,
            id_empleado=self.empleado
        )
        self.detalle_data = {
            'cantidad': 2,
            'precio_unitario': 10.50,
            'id_factura': self.factura.id,
            'id_producto': self.producto.id
        }
        self.detalle = DetalleVenta.objects.create(
            cantidad=1,
            precio_unitario=10.50,
            id_factura=self.factura,
            id_producto=self.producto
        )

    def test_crear_detalle(self):
        url = reverse('detalleventa-list')
        response = self.client.post(url, self.detalle_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DetalleVenta.objects.count(), 2)

        # Usar latest('id') para obtener el último detalle creado
        ultimo_detalle = DetalleVenta.objects.latest('id')
        self.assertEqual(ultimo_detalle.cantidad, 2)

    def test_listar_detalles(self):
        url = reverse('detalleventa-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_obtener_detalle(self):
        url = reverse('detalleventa-detail', args=[self.detalle.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_eliminar_detalle(self):
        url = reverse('detalleventa-detail', args=[self.detalle.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DetalleVenta.objects.count(), 0)

class MovimientoTests(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Medicamentos')
        self.proveedor = Proveedor.objects.create(nombre='Proveedor Ejemplo', contacto='contacto@ejemplo.com')
        self.producto = Producto.objects.create(
            nombre='Paracetamol',
            precio=10.50,
            stock=100,
            id_categoria=self.categoria,
            id_proveedor=self.proveedor
        )
        self.cliente = Cliente.objects.create(nombre='Carlos López', correo='carlos@example.com', telefono='3101234567')
        self.movimiento_data = {
            'tipo': 'entrada',
            'cantidad': 10,
            'id_producto': self.producto.id,
            'id_cliente': self.cliente.id
        }
        self.movimiento = Movimiento.objects.create(
            tipo='salida',
            cantidad=5,
            id_producto=self.producto,
            id_cliente=self.cliente
        )

    def test_crear_movimiento(self):
        url = reverse('movimiento-list')
        response = self.client.post(url, self.movimiento_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movimiento.objects.count(), 2)

        # Usar latest('id') para obtener el último movimiento creado
        ultimo_movimiento = Movimiento.objects.latest('id')
        self.assertEqual(ultimo_movimiento.tipo, 'entrada')

    def test_listar_movimientos(self):
        url = reverse('movimiento-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_obtener_movimiento(self):
        url = reverse('movimiento-detail', args=[self.movimiento.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_eliminar_movimiento(self):
        url = reverse('movimiento-detail', args=[self.movimiento.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movimiento.objects.count(), 0)
