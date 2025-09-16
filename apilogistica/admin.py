from django.contrib import admin
from .models import (
    Origen,
    Productos,
    Lista_productos_negados,
    Lista_productos_pedidos,
    Cuidad,
    Zona,
    Asociado,
    Vendedor,
    Conductor,
    Facturas_contabilidad
)


admin.site.register(Origen)
admin.site.register(Productos)
admin.site.register(Lista_productos_negados)
admin.site.register(Lista_productos_pedidos)
admin.site.register(Cuidad)
admin.site.register(Zona)
admin.site.register(Asociado)
admin.site.register(Vendedor)
admin.site.register(Conductor)
admin.site.register(Facturas_contabilidad)