from django.test import TestCase
from datetime import date
from decimal import Decimal
from django.db.utils import IntegrityError 
from procesamiento.models import ProductoNegado, pickingModel 


class ProductoNegadoModelTest(TestCase):
    """Pruebas unitarias para el modelo ProductoNegado"""

    def setUp(self):
        self.producto = ProductoNegado.objects.create(
            fecha=date(2025, 10, 23),
            producto="CONCENTRADO PREMIUM 25KG",
            marca="BIOS",
            cantidad_negada=Decimal("5.50"),
            origen="S123456",
            referencia="REF-999"
        )

    def test_creacion_correcta(self):
        """Debe crear un producto negado correctamente"""
        self.assertEqual(self.producto.producto, "CONCENTRADO PREMIUM 25KG")
        self.assertEqual(self.producto.marca, "BIOS")
        self.assertEqual(self.producto.cantidad_negada, Decimal("5.50"))
        self.assertEqual(self.producto.origen, "S123456")
        self.assertEqual(self.producto.referencia, "REF-999")
        self.assertIsInstance(self.producto.fecha, date)

    def test_str_representation(self):
        """Debe mostrar el formato correcto en __str__"""
        expected_str = f"{self.producto.origen} - {self.producto.marca} ({self.producto.fecha})"
        self.assertEqual(str(self.producto), expected_str)

    def test_campos_requeridos(self):
        """No debe permitir campos requeridos vacíos (Prueba Corregida)"""
        # Se fuerza el campo 'origen' a None para asegurar que el ORM intente
        # insertar NULL, disparando el IntegrityError de la BD.
        with self.assertRaises(IntegrityError): 
            ProductoNegado.objects.create(
                fecha=date.today(),
                producto="Sin origen",
                marca="Marca X",
                cantidad_negada=Decimal("1.00"),
                referencia="SINREF",
                # 🚨 Campo faltante con valor explícito None
                origen=None 
            )


class PickingModelTest(TestCase):
    """Pruebas unitarias para el modelo pickingModel"""

    def setUp(self):
        self.picking = pickingModel.objects.create(
            nombreAsociado="Juan Pérez",
            fechaFactura=date(2025, 10, 23),
            identificacionAsociado="1234567890",
            vendedor="Carlos Gómez",
            cantidad=Decimal("25.00"),
            producto="CONCENTRADO PREMIUM 25KG",
            pesoUnitario=Decimal("25.00"),
            cuidad="Bogotá",
            codigoZona="Z-01",
            zona="Centro",
            origen="S987654",
            marca="BIOS",
            idOdoo="ODOO-1234"
        )

    def test_creacion_correcta(self):
        """Debe crear un registro picking correctamente"""
        self.assertEqual(self.picking.nombreAsociado, "Juan Pérez")
        self.assertEqual(self.picking.vendedor, "Carlos Gómez")
        self.assertEqual(self.picking.zona, "Centro")
        self.assertEqual(self.picking.cantidad, Decimal("25.00"))
        self.assertEqual(self.picking.origen, "S987654")

    def test_str_representation(self):
        """Debe mostrar el formato correcto en __str__"""
        expected_str = f"{self.picking.origen} - {self.picking.zona} ({self.picking.fechaFactura})"
        self.assertEqual(str(self.picking), expected_str)

    def test_fecha_procesamiento_auto(self):
        """Debe asignar automáticamente la fecha de procesamiento"""
        self.assertIsNotNone(self.picking.fecha_procesamiento)
        self.assertIsInstance(self.picking.fecha_procesamiento, date)

    def test_valores_decimal(self):
        """Los valores de cantidad y pesoUnitario deben ser decimales"""
        self.assertIsInstance(self.picking.cantidad, Decimal)
        self.assertIsInstance(self.picking.pesoUnitario, Decimal)

    def test_campo_obligatorio(self):
        """Debe lanzar error si falta un campo requerido (Prueba Corregida)"""
        # Se fuerza el campo 'origen' a None para disparar el IntegrityError
        with self.assertRaises(IntegrityError):
            pickingModel.objects.create(
                nombreAsociado="Sin Origen",
                fechaFactura=date.today(),
                identificacionAsociado="000",
                vendedor="Vendedor X",
                cantidad=Decimal("10.00"),
                producto="Prueba",
                pesoUnitario=Decimal("10.00"),
                cuidad="Cali",
                codigoZona="Z-02",
                zona="Sur",
                marca="Test",
                idOdoo="OD-000",
                origen=None 
            )