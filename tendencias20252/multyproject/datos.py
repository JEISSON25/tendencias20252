# seed_data.py
import os
import sys
import django
from datetime import date

# Add the project directory to the Python import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multyproject.settings')
django.setup()

from apilogistica.models import (
    Origen, Productos, Lista_productos_negados, Lista_productos_pedidos,
    Cuidad, Zona, Asociado, Vendedor, Conductor, Facturas_contabilidad
)

def run():
    try:
        # Delete existing data to prevent duplicates
        print("Eliminando datos existentes...")
        Facturas_contabilidad.objects.all().delete()
        Lista_productos_negados.objects.all().delete()
        Lista_productos_pedidos.objects.all().delete()
        Productos.objects.all().delete()
        Asociado.objects.all().delete()
        Cuidad.objects.all().delete()
        Zona.objects.all().delete()
        Origen.objects.all().delete()
        Vendedor.objects.all().delete()
        Conductor.objects.all().delete()

        # Create new data
        print("Creando datos de origen...")
        origen_1 = Origen.objects.create(origen='MEDELLIN')
        origen_2 = Origen.objects.create(origen='BOGOTA')

        print("Creando datos de ciudad...")
        cuidad_1 = Cuidad.objects.create(cuidad='Medellín')
        cuidad_2 = Cuidad.objects.create(cuidad='Bogotá')

        print("Creando datos de zona...")
        zona_1 = Zona.objects.create(zona='Zona Norte')
        zona_2 = Zona.objects.create(zona='Zona Sur')

        print("Creando datos de asociado...")
        asociado_1 = Asociado.objects.create(
            cedula_Asociado='123456789', 
            nombre_Asociado='Juan Pérez', 
            cuidad=cuidad_1, 
            Zona=zona_1
        )
        asociado_2 = Asociado.objects.create(
            cedula_Asociado='987654321', 
            nombre_Asociado='María López', 
            cuidad=cuidad_2, 
            Zona=zona_2
        )

        print("Creando datos de vendedor...")
        vendedor_1 = Vendedor.objects.create(vendedor='Ana Gomez')
        vendedor_2 = Vendedor.objects.create(vendedor='Luis Diaz')

        print("Creando datos de conductor...")
        conductor_1 = Conductor.objects.create(conductor='Carlos Montoya')
        conductor_2 = Conductor.objects.create(conductor='Felipe Vargas')

        print("Creando datos de productos...")
        producto_1 = Productos.objects.create(
            producto_referencia='REF001', 
            producto_nombre='Azúcar', 
            marca='Marca A', 
            precio_ponderado=2500.50, 
            peso_unitario=1000.00
        )
        producto_2 = Productos.objects.create(
            producto_referencia='REF002', 
            producto_nombre='Harina', 
            marca='Marca B', 
            precio_ponderado=3000.75, 
            peso_unitario=500.50
        )

        print("Creando datos de lista de productos negados...")
        lista_negada_1 = Lista_productos_negados.objects.create(
            producto_referencia=producto_1, 
            origen=origen_1, 
            cantidad_negada=15.00
        )
        lista_negada_2 = Lista_productos_negados.objects.create(
            producto_referencia=producto_2, 
            origen=origen_2, 
            cantidad_negada=5.00
        )

        print("Creando datos de lista de productos pedidos...")
        lista_pedida_1 = Lista_productos_pedidos.objects.create(
            producto_referencia=producto_1, 
            origen=origen_1, 
            cantidad_pedida=100.00, 
            precio_venta=2800.00
        )
        lista_pedida_2 = Lista_productos_pedidos.objects.create(
            producto_referencia=producto_2, 
            origen=origen_2, 
            cantidad_pedida=50.00, 
            precio_venta=3200.00
        )

        print("Creando datos de facturas de contabilidad...")
        factura_1 = Facturas_contabilidad.objects.create(
            origen=origen_1, 
            fecha_factura=date(2025, 9, 13), 
            cedula_Asociado=asociado_1, 
            vendedor=vendedor_1, 
            peso_total=5000.00, 
            precio_total=140000.00, 
            id_importacion='IMP-2025-001', 
            estado_orden=True, 
            conductor=conductor_1
        )
        factura_2 = Facturas_contabilidad.objects.create(
            origen=origen_2, 
            fecha_factura=date(2025, 9, 12), 
            cedula_Asociado=asociado_2, 
            vendedor=vendedor_2, 
            peso_total=2500.00, 
            precio_total=80000.00, 
            id_importacion='IMP-2025-002', 
            estado_orden=False, 
            conductor=conductor_2
        )

        print("¡Se ha completado la siembra de datos exitosamente!")

    except Exception as e:
        print(f"Ocurrió un error durante la siembra de datos: {e}")

if __name__ == "__main__":
    run()