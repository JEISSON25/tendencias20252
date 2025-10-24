from django.contrib import admin
from .models import Productos
from .models import Cliente
from .models import Venta
from .models import DetalleVenta    

admin.site.register(Productos)
admin.site.register(Cliente)
admin.site.register( Venta )
admin.site.register( DetalleVenta )
# Register your models here.
