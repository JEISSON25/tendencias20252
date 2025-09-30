# resources.py
from import_export import resources, fields
from tablib import Dataset
import pandas as pd

from .models import ProductoNegado
from .utils import limpiar_y_preparar_detalle


class ProductoNegadoResource(resources.ModelResource):
    # Campos alineados al modelo
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
