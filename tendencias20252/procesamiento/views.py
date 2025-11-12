import os
import pandas as pd
import numpy as np
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db import transaction
from .models import ProductoNegado, pickingModel, CortesLogistico
from .serializer import ProductoNegadoSerializer, PickingSerializer, PickingPatchSerializer, CortesLogisticoSerializer
from .utils.utilsimport import limpiar_y_preparar_detalle, pickingPacking
from .filters import PickingFilter
from rest_framework.permissions import IsAuthenticated
import django_filters.rest_framework

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
    ordering = ["-fecha"] # orden por defecto (más recientes primero)
    
class CortesLogisticoViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    
    queryset = CortesLogistico.objects.all()
    serializer_class = CortesLogistico

    # 👉 Aquí agregamos filtros genéricos
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Campos por los que se puede filtrar (ej: exact match)
    filterset_fields = ["nombre", "fecha"]  

    # Campos para búsqueda (ej: contiene, insensible a mayúsculas/minúsculas)
    search_fields = ["nombre", "fecha"] 

    # Campos para ordenar resultados
    ordering_fields = ["fecha"]
    ordering = ["-fecha"]
    

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

class CortesLogisticoView(APIView):    
    def post(self, request, *args, **kwargs):
        serializer = CortesLogisticoSerializer(data=request.data)
        
        if serializer.is_valid():
            instance = serializer.save()
            
            
            return Response({
                "status": "ok",
                "mensaje": "El corte logístico ha sido guardado con éxito.",
                "datos_creados": serializer.data, 
                "id_creado": instance.pk 
            }, status=status.HTTP_201_CREATED)
        
    
        return Response(
            {
                "error": "Error de validación de datos.", 
                "detalle": serializer.errors
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )  
        
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

            registros_finales = df_crudo.to_dict(orient='records')
            serializer = ProductoNegadoSerializer(data=registros_finales, many=True)
            
            if not serializer.is_valid():
                return Response(
                    {"error_logica": "Fallo en la conversión de tipos post-limpieza", 
                     "detalle_drf": serializer.errors}, 
                    status=status.HTTP_400_BAD_REQUEST)
                
                
                            
            # --- Generación del Resumen (Para devolver en la respuesta) ---
            df_resumen = df_crudo
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
        print("🔍 Primer registro recibido:", datos_recibidos_crudos[0].keys())
        
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
                print("❌ Errores del serializer:", serializer.errors) 
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
            
   
class ReporteDatosView(ListAPIView):
    queryset = pickingModel.objects.all().order_by('-fechaFactura') 
    serializer_class = PickingSerializer
    permission_classes = [IsAuthenticated] 
    
    # ✅ Aplicar los backends de filtro
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = PickingFilter

class ActualizarPickingMasivoView(APIView):
    """
    Vista para recibir una petición PATCH masiva desde st.data_editor
    y actualizar los registros identificados por su ID interno (PK).
    """
    permission_classes = [IsAuthenticated] 

    def patch(self, request, *args, **kwargs):
        data = request.data 
        
        # 1. Validar la lista de cambios (con many=True)
        serializer = PickingPatchSerializer(data=data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        updates = []
        
        try:
            # 2. Transacción Atómica: Asegura que todos los cambios pasen o fallen
            with transaction.atomic():
                for item in serializer.validated_data:
                    id_registro_pk = item.pop('id') 
                    fields_to_update = {k: v for k, v in item.items() if v is not None}
                    
                    if fields_to_update:
                        pickingModel.objects.filter(pk=id_registro_pk).update(**fields_to_update)
                        updates.append(id_registro_pk)
            
            return Response({
                "status": "success", 
                "message": f"Actualizaciones aplicadas a {len(updates)} registros.",
                "registros_actualizados": updates
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error durante la actualización masiva: {e}")
            return Response({
                "status": "error",
                "message": f"Fallo en la actualización masiva: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)