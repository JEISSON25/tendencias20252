import os
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.db.models.functions import Coalesce
from .models import ProductoNegado
from .serializer import ProductoNegadoSerializer
from .utils import limpiar_y_preparar_detalle



class ProductoNegadoViewSet(viewsets.ModelViewSet):
    queryset = ProductoNegado.objects.all()
    serializer_class = ProductoNegadoSerializer

    # 👉 Aquí agregamos filtros genéricos
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Campos por los que se puede filtrar (ej: exact match)
    filterset_fields = ["marca", "Fecha"]  

    # Campos para búsqueda (ej: contiene, insensible a mayúsculas/minúsculas)
    search_fields = ["Movimientos_de_Existencias_Descripcion", "Documento_Origen"]

    # Campos para ordenar resultados
    ordering_fields = ["Fecha", "Producto_negado"]
    ordering = ["-Fecha"]  # orden por defecto (más recientes primero)



class UploadExcelProductoNegadoView(APIView):
    def post(self, request):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No se envió archivo"}, status=status.HTTP_400_BAD_REQUEST)

        path = os.path.join(settings.MEDIA_ROOT, file_obj.name)
        with open(path, "wb+") as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)

        # Procesar y limpiar datos
        df = limpiar_y_preparar_detalle(path)

        # Guardar en BD
        movimientos = [
            ProductoNegado(
                fecha=row["Fecha"],
                descripcion=row["Movimientos de Existencias/Descripción"],
                cantidad_real=row["Movimientos de Existencias/Cantidad Real"],
                cantidad_reservada=row["Movimientos de Existencias/Cantidad Reservada"],
                producto_negado=row["Producto negado"],
                marca=row["marca"],
                documento_origen=row["Documento Origen"],
                referencia=row["Referencia"]
            )
            for _, row in df.iterrows()
        ]
        ProductoNegado.objects.bulk_create(movimientos)

        return Response({
            "status": "ok",
            "filas_guardadas": len(movimientos)
        }, status=status.HTTP_201_CREATED)



class ReporteNegadosView(APIView):
    def get(self, request):
        resumen = (
            ProductoNegado.objects
            .values("marca", "descripcion")
            .annotate(
                unidades_negadas=Coalesce(Sum("producto_negado"), 0),
            )
            .order_by("-unidades_negadas")
        )

        return Response(list(resumen))
