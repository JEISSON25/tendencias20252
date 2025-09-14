import datetime

from rest_framework import status
from rest_framework.response import Response
from ..serializers import BookingSerializer

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from django.http import HttpResponse

def generate_json_report(queryset):
    """
    Función para generar reportes en formato JSON.
    """
    serializer = BookingSerializer(queryset, many=True)
    return Response(serializer.data)

def generate_pdf_report(queryset):
    """
    Función para generar reportes en formato PDF.
    """    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_reservas.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)
    
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], alignment=1, fontSize=18, spaceAfter=12, textColor=colors.HexColor('#003366'))
    subtitle_style = ParagraphStyle('SubtitleStyle', parent=styles['Normal'], alignment=1, fontSize=10, textColor=colors.gray)
    
    elements.append(Paragraph("Reporte de Reservas", title_style))
    elements.append(Paragraph(f"Generado el: {datetime.date.today().strftime('%d-%m-%Y')}", subtitle_style))
    elements.append(Spacer(1, 12))

    data = [['ID', 'Usuario', 'Servicio', 'Inicio', 'Fin', 'Costo Final']]
    for booking in queryset:
        data.append([
            booking.id,
            booking.user.username,
            booking.service_instance.name,
            booking.start_time.strftime('%Y-%m-%d %H:%M'),
            booking.end_time.strftime('%Y-%m-%d %H:%M'),
            f"${booking.final_cost}"
        ])

    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 0), (-1, 0), 10),

        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),

        # Alternar colores de fila
        ('BACKGROUND', (0, 2), (-1, -1), colors.white),
        
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CCCCCC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
    ])

    table = Table(data)
    table.setStyle(table_style)
    elements.append(table)

    # Construir el documento
    doc.build(elements)

    return response