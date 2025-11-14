import json
from rest_framework import viewsets
from .models import Reservas
from apps.logs.utils import crear_log
from .serializers import ReservasSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
# Para PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse


class ReservasViewSet(viewsets.ModelViewSet):
    queryset = Reservas.objects.all()
    serializer_class = ReservasSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter] 
    filterset_fields = ('__all__')
    search_fields = ('__all__')
    ordering_fields = ('__all__')

    def perform_create(self, serializer):
        reserva = serializer.save()

        crear_log(
            usuario=self.request.user,
            status="success",
            level="reservas",
            message=(
                f"Creó una reserva ({reserva.id_reserva}) "
                f"para el recurso '{reserva.id_recurso.nombre_recurso}' "
            )
        )


    def perform_update(self, serializer):
        reserva = serializer.save()

        crear_log(
            usuario=self.request.user,
            status="success",
            level="reservas",
            message=(
                f"Actualizó la reserva ({reserva.id_reserva}) "
                f"del recurso '{reserva.id_recurso.nombre_recurso}' "
            )
        )
 
    def perform_destroy(self, instance):

        crear_log(
            usuario=self.request.user,
            status="warning",
            level="reservas",
            message=(
                f"Eliminó la reserva ({instance.id_reserva}) "
                f"del recurso '{instance.id_recurso.nombre_recurso}'"
            )
        )

        instance.delete()



def reservas_view(request):
    return render(request, 'reservas.html')

def export_reservas_to_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    reservas = Reservas.objects.all()
    y = height - 40
    p.setFont("Helvetica", 12)
    p.drawString(250, y, "Listado de Reservas")

    p.drawString(30, 730, "ID")
    p.drawString(100, 730, "usuario")
    p.drawString(220, 730, "rol usuario")
    p.drawString(300, 730, "Tipo recurso")
    
    y = 710

    for reserva in reservas:
        p.drawString(30, y, reserva.id_reserva.__str__())
        p.drawString(100, y, reserva.id_user.username)
        p.drawString(220, y, reserva.id_user.rol.nombre_rol)
        p.drawString(300, y, reserva.id_recurso.tipo_recurso) 
        y -= 20

        if y < 100:
            p.showPage()
            p.setFont("Helvetica", 10)
            y = 750

    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')



def export_reservas_to_json(request):
    reservas = Reservas.objects.all()
    data = []  

    for reserva in reservas:
        data.append({
            'id_reserva': reserva.id_reserva,
            'estado_reserva': reserva.estado_reserva,
            'id_user': reserva.id_user.username,
            'tipo_recurso': reserva.id_recurso.tipo_recurso,
            'fecha_inicio': reserva.fecha_inicio.isoformat(),
            'fecha_fin': reserva.fecha_fin.isoformat(),
        })

    response = HttpResponse(
        json.dumps(data, indent=4, ensure_ascii=False),
        content_type='application/json'
    )
    #response['Content-Disposition'] = 'attachment; filename="productos.json"'
    
    return response
