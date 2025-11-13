# apps/ventas/views_reportes.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from rest_framework.exceptions import NotAcceptable

from .models import Venta
from .serializers import VentaSerializer
from .reports import ventas_pdf


class ReporteVentas(APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    #IGNORAR NEGOTIATION CUANDO ?format=pdf
    def perform_content_negotiation(self, request, *args, **kwargs):
        fmt = request.GET.get("format")
        if fmt == "pdf":
            # evita que DRF intente seleccionar renderer
            return (None, None)
        return super().perform_content_negotiation(request, *args, **kwargs)

    def get_queryset(self, request):
        qs = (
            Venta.objects
            .select_related('cliente', 'vendedor')
            .prefetch_related('detalles__producto')
            .all()
        )

        f = request.GET.get("from")
        t = request.GET.get("to")

        if f:
            qs = qs.filter(fecha__date__gte=parse_date(f))
        if t:
            qs = qs.filter(fecha__date__lte=parse_date(t))

        return qs.order_by("fecha")

    def get(self, request, *args, **kwargs):
        fmt = request.GET.get("format", "json").lower()
        qs = self.get_queryset(request)

        if fmt == "pdf":
            pdf_bytes = ventas_pdf(qs)
            return HttpResponse(
                pdf_bytes,
                content_type="application/pdf",
                headers={
                    "Content-Disposition": 'attachment; filename="reporte_ventas.pdf"'
                }
            )

        data = VentaSerializer(qs, many=True).data
        return Response({"count": len(data), "results": data})
