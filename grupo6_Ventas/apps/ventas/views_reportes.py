# apps/ventas/views_reportes.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.utils.dateparse import parse_date

from .models import Venta
from .serializers import VentaSerializer
from .reports import ventas_pdf

class ReporteVentas(APIView):
   
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        qs = (Venta.objects
              .select_related('cliente', 'vendedor')
              .prefetch_related('detalles__producto')
              .all())
        f = request.GET.get('from')
        t = request.GET.get('to')
        if f:
            qs = qs.filter(fecha__date__gte=parse_date(f))
        if t:
            qs = qs.filter(fecha__date__lte=parse_date(t))
        return qs.order_by('fecha')

    def get(self, request, *args, **kwargs):
        fmt = (request.GET.get('format') or 'json').lower()
        qs = self.get_queryset(request)
        if fmt == 'pdf':
            pdf_bytes = ventas_pdf(qs)
            resp = HttpResponse(pdf_bytes, content_type='application/pdf')
            resp['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'
            return resp
        data = VentaSerializer(qs, many=True).data
        return Response({"count": len(data), "results": data})
