# resources.py
from import_export import resources, fields
from tablib import Dataset
import pandas as pd

from .models import ProductoNegado, pickingModel
from .utils.utilsimport import limpiar_y_preparar_detalle, pickingPacking


class ProductoNegadoResource(resources.ModelResource):
    fecha = fields.Field(attribute="fecha")
    producto = fields.Field(attribute="producto")
    cantidad_negada = fields.Field(attribute="cantidad_negada")
    marca = fields.Field(attribute="marca")
    origen = fields.Field(attribute="origen")
    referencia = fields.Field(attribute="referencia")

    class Meta:
      model = ProductoNegado
      fields = ("fecha", "producto", "cantidad_negada", "marca", "origen", "referencia")
      exclude = ("id",)
      import_id_fields = ()
      
    def before_import(self, dataset: Dataset, **kwargs):
      df = pd.DataFrame(dataset.dict)

    # Eliminar 'id' si viene en el archivo
      if "id" in df.columns:
        df = df.drop(columns=["id"])

      detalle = limpiar_y_preparar_detalle(df)

      dataset.dict = detalle.to_dict(orient="records")

class pickingResource(resources.ModelResource):
    # Campos alineados al modelo
    nombreAsociado = fields.Field(attribute="nombreAsociado")
    fechaFactura = fields.Field(attribute="fechaFactura")
    identificacionAsociado = fields.Field(attribute="identificacionAsociado")
    vendedor = fields.Field(attribute="vendedor")
    cantidad = fields.Field(attribute="cantidad")
    producto = fields.Field(attribute="producto")
    pesoUnitario = fields.Field(attribute="pesoUnitario")
    cuidad = fields.Field(attribute="cuidad")
    codigoZona = fields.Field(attribute="codigoZona")
    zona = fields.Field(attribute="zona")
    origen = fields.Field(attribute="origen")
    marca = fields.Field(attribute="marca")
    idOdoo= fields.Field(attribute="idOdoo")
    

    class Meta:
      model = pickingModel
      fields = ("nombreAsociado","fechaFactura","identificacionAsociado","vendedor","cantidad","producto",
            "pesoUnitario","cuidad","codigoZona","zona","origen","marca","idOdoo")
      exclude = ("id",)
      import_id_fields = ()
      
    def before_import(self, dataset: Dataset, **kwargs):
      df = pd.DataFrame(dataset.dict)

    # Eliminar 'id' si viene en el archivo
      if "id" in df.columns:
        df = df.drop(columns=["id"])

      pick = pickingPacking(df)

      dataset.dict = pick.to_dict(orient="records")
