# admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import XLSX  # 👈 importa el formato

from .models import ProductoNegado, pickingModel
from .resources import ProductoNegadoResource, pickingResource


@admin.register(ProductoNegado)
class ProductoNegadoAdmin(ImportExportModelAdmin):
    resource_class = ProductoNegadoResource
    list_display = ("fecha", "producto", "marca", "cantidad_negada", "origen", "referencia")

    def get_export_formats(self):
        return [XLSX]  # 👈 usa la clase, no el objeto

    def get_import_formats(self):
        return [XLSX]  # 👈 idem aquí
    

@admin.register(pickingModel)
class pickingAdmin(ImportExportModelAdmin):
    resource_class = pickingResource
    list_display = ("nombreAsociado","fechaFactura","identificacionAsociado","vendedor","cantidad","producto",
            "pesoUnitario","cuidad","codigoZona","zona","origen","marca","idOdoo")

    def get_export_formats(self):
        return [XLSX]  # 👈 usa la clase, no el objeto

    def get_import_formats(self):
        return [XLSX]  # 👈 idem aquí
