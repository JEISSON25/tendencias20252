import json
from rest_framework import viewsets
from .models import Recursos
from .serializers import RecursosSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
# Para PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse


class RecursosViewSet(viewsets.ModelViewSet):
    queryset = Recursos.objects.all()
    serializer_class = RecursosSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] 
    filterset_fields = ('__all__')
    search_fields = ('__all__')
    ordering_fields = ('__all__')


def export_recursos_to_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    recursos = Recursos.objects.all()
    y = height - 40
    p.setFont("Helvetica", 12)
    p.drawString(250, y, "Listado de Recursos")

    p.drawString(30, 730, "ID")
    p.drawString(100, 730, "Nombre")
    p.drawString(220, 730, "Estado")
    p.drawString(300, 730, "Descripción")
    
    y = 710

    for recurso in recursos:
        p.drawString(30, y, recurso.id_recurso)
        p.drawString(100, y, recurso.nombre_recurso)
        p.drawString(220, y, recurso.estado_recurso)
        p.drawString(300, y, recurso.descripcion_recurso) 
        y -= 20

        if y < 100:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = 750

    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


def export_recursos_to_json(request):
    recursos = Recursos.objects.all()
    data = []  

    for recurso in recursos:
        data.append({
            'id_recurso': recurso.id_recurso,
            'nombre_recurso': recurso.nombre_recurso,
            'estado_recurso': recurso.estado_recurso,
            'descripcion_recurso': recurso.descripcion_recurso,
        })

    response = HttpResponse(
        json.dumps(data, indent=4, ensure_ascii=False),
        content_type='application/json'
    )
    #response['Content-Disposition'] = 'attachment; filename="productos.json"'
    
    return response
