import os
import pandas as pd
import numpy as np
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.db.models.functions import Coalesce
from .models import ProductoNegado, pickingModel
from .serializer import ProductoNegadoSerializer, PickingSerializer
from .utils.utilsimport import limpiar_y_preparar_detalle, pickingPacking
from rest_framework.permissions import IsAuthenticated

#Variable global
NAN_PLACEHOLDER = "__NAN_PLACEHOLDER__"

class ProductoNegadoViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    
    queryset = ProductoNegado.objects.all()
    serializer_class = ProductoNegadoSerializer

    # 👉 Aquí agregamos filtros genéricos
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Campos por los que se puede filtrar (ej: exact match)
    filterset_fields = ["marca", "fecha"]  

    # Campos para búsqueda (ej: contiene, insensible a mayúsculas/minúsculas)
    search_fields = ["producto", "origen"]

    # Campos para ordenar resultados
    ordering_fields = ["fecha", "producto"]
    ordering = ["-fecha"]  # orden por defecto (más recientes primero)

class PickingViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    
    
    queryset = pickingModel.objects.all()
    serializer_class = PickingSerializer

    # 👉 Aquí agregamos filtros genéricos
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Campos por los que se puede filtrar (ej: exact match)
    filterset_fields = ["marca", "fechaFactura"]  

    # Campos para búsqueda (ej: contiene, insensible a mayúsculas/minúsculas)
    search_fields = ["producto", "origen"]

    # Campos para ordenar resultados
    ordering_fields = ["fechaFactura", "producto"]
    ordering = ["-fechaFactura"]  


class UploadExcelProductoNegadoView(APIView):
    def post(self, request, *args, **kwargs):
        
        datos_recibidos_crudos = request.data
        
        # 1. Validación inicial: Asegurar que es una lista
        if not isinstance(datos_recibidos_crudos, list):
             return Response(
                {"error": "Se esperaba una lista de registros JSON."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 2. Convertir a DataFrame y REVERTIR el placeholder de NaN
            df_crudo = pd.DataFrame(datos_recibidos_crudos)
            df_crudo = df_crudo.replace(NAN_PLACEHOLDER, np.nan) 
            # 3. Procesar y limpiar datos (TU LÓGICA DE NEGOCIO REAL)
            # Esta función DEBE validar, convertir tipos y rellenar los nulos (np.nan).
            df_limpio = limpiar_y_preparar_detalle(df_crudo)
            
            # 4. (Opcional) Validar la estructura final con el Serializador
            # Si quieres usar el Serializador como un 'check' final de tipos antes de guardar
            registros_finales = df_limpio.to_dict(orient='records')
            serializer = ProductoNegadoSerializer(data=registros_finales, many=True)
            
            if not serializer.is_valid():
                return Response(
                    {"error_logica": "Fallo en la conversión de tipos post-limpieza", 
                     "detalle_drf": serializer.errors}, 
                    status=status.HTTP_400_BAD_REQUEST)
                
                
                            
            # --- Generación del Resumen (Para devolver en la respuesta) ---
            df_resumen = df_limpio.groupby(
                by=["marca", "producto"]
            )["cantidad_negada"].sum().reset_index()
            datos_resumen_json = df_resumen.to_dict(orient='records')
            # -------------------------------------------------------------
            
            #Metodo para guardar los datos
            movimientos = [ProductoNegado(**registro) for registro in serializer.validated_data]
            ProductoNegado.objects.bulk_create(movimientos)

            # 🟢 Incluir el resumen en la respuesta del POST 
            return Response({
                "status": "ok",
                "filas_guardadas": len(movimientos),
                "mensaje": "Datos procesados y guardados con éxito.",
                "resumen_procesado": datos_resumen_json 
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Captura errores que ocurran durante el procesamiento o el bulk_create
            print(f"Error en el procesamiento o base de datos: {e}")
            return Response({
                "status": "error",
                "detalle": f"Error interno en el procesamiento: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReportenegadosView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # 1. Obtener datos y serializar
            datos = ProductoNegado.objects.all()
            serializer = ProductoNegadoSerializer(datos, many=True)
            df = pd.DataFrame(serializer.data)

            # 2. Procesamiento (Group By en el Backend)
            df_resumen = df.groupby(
                by=["marca", "producto"]
            )["cantidad_negada"].sum().reset_index()
            
            # 3. Preparar la respuesta HTTP como JSON (en lugar de PDF)
            
            # Convertimos el DataFrame agrupado a una lista de diccionarios JSON
            datos_resumen_json = df_resumen.to_dict(orient='records')
            
            # Devolvemos la respuesta JSON con código 200 OK
            return Response(datos_resumen_json, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "detalle": f"Error al generar el resumen: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#Organizar estas vistas
class UploadPickinView(APIView):
    def post(self, request, *args, **kwargs):
        
        datos_recibidos_crudos = request.data
        
        # 1. Validación inicial: Asegurar que es una lista
        if not isinstance(datos_recibidos_crudos, list):
             return Response(
                {"error": "Se esperaba una lista de registros JSON."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 2. Convertir a DataFrame y REVERTIR el transformación de NaN
            df_crudo = pd.DataFrame(datos_recibidos_crudos)
            df_crudo = df_crudo.replace(NAN_PLACEHOLDER, np.nan)  
            # 3. Procesar y limpiar datos (TU LÓGICA DE NEGOCIO REAL)
            
            df_limpio = pickingPacking(df_crudo)
            
            # 4. (Opcional) Validar la estructura final con el Serializador
            # Si quieres usar el Serializador como un 'check' final de tipos antes de guardar
            registros_finales = df_limpio.to_dict(orient='records')
            serializer = PickingSerializer(data=registros_finales, many=True)
            
            if not serializer.is_valid():
                return Response(
                    {"error_logica": "Fallo en la conversión de tipos post-limpieza", 
                     "detalle_drf": serializer.errors}, 
                    status=status.HTTP_400_BAD_REQUEST)
                
                
                            
            # --- Generación del Resumen (Para devolver en la respuesta) ---
            df_resumen = df_limpio.reset_index()
            
            datos_resumen_json = df_resumen.to_dict(orient='records')
            # -------------------------------------------------------------
            
            #Metodo para guardar los datos
            movimientos = [pickingModel(**registro) for registro in serializer.validated_data]
            pickingModel.objects.bulk_create(movimientos)

            # 🟢 Incluir el resumen en la respuesta del POST 
            return Response({
                "status": "ok",
                "filas_guardadas": len(movimientos),
                "mensaje": "Datos procesados y guardados con éxito.",
                "resumen_procesado": datos_resumen_json 
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Captura errores que ocurran durante el procesamiento o el bulk_create
            print(f"Error en el procesamiento o base de datos: {e}")
            return Response({
                "status": "error",
                "detalle": f"Error interno en el procesamiento: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
   

class ReporteNegadosView(APIView):
    def get(self, request):
        resumen = (
            pickingModel.objects
            .values("zona", "marca")
            .annotate(
                unidades_pedidas=Coalesce(Sum("cantidad"), 0),
            )
            .order_by("-cantidad")
        )

        return Response(list(resumen))

