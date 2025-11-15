import datetime

from rest_framework import status
from rest_framework.response import Response
from ..serializers import BookingSerializer

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from django.http import HttpResponse
from django.utils import timezone
from decimal import Decimal

def generate_json_report(queryset):
    """
    Función para generar reportes en formato JSON.
    """
    serializer = BookingSerializer(queryset, many=True)
    return Response(serializer.data)

def generate_pdf_report(queryset, filters=None):
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

    brand_primary = colors.HexColor('#4A7C59')
    brand_secondary = colors.HexColor('#8B5E3C')
    brand_muted = colors.HexColor('#9CA3AF')
    brand_surface = colors.HexColor('#F4F1ED')

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=20,
        textColor=brand_primary,
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=10,
        textColor=brand_muted,
        spaceAfter=16,
    )
    section_title_style = ParagraphStyle(
        'SectionTitleStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=brand_secondary,
        spaceBefore=18,
        spaceAfter=8,
    )
    footnote_style = ParagraphStyle(
        'FootnoteStyle',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_RIGHT,
        textColor=brand_muted,
        spaceBefore=12,
    )
    
    elements.append(Paragraph("Reporte de Reservas", title_style))
    elements.append(Paragraph(f"Generado el {timezone.now().strftime('%d/%m/%Y %H:%M')}", subtitle_style))

    total_reservas = queryset.count()
    total_horas = sum((booking.end_time - booking.start_time).total_seconds() / 3600 for booking in queryset)
    total_ingresos = sum((booking.final_cost or Decimal('0.00')) for booking in queryset)

    summary_data = [
        ["Total de reservas", f"{total_reservas:,}".replace(",", ".")],
        ["Horas reservadas", f"{total_horas:.1f} h"],
        ["Ingresos estimados", f"${total_ingresos:.2f}"],
    ]

    summary_table = Table(summary_data, colWidths=[2.7 * inch, 2.8 * inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), brand_surface),
        ('TEXTCOLOR', (0, 0), (-1, -1), brand_secondary),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
        ('BOX', (0, 0), (-1, -1), 0.5, brand_secondary),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(summary_table)
    if filters:
        filter_lines = [f"{label}: {value}" for label, value in filters]
        filter_paragraph = Paragraph(
            "Filtros aplicados: " + " | ".join(filter_lines),
            ParagraphStyle(
                'FilterStyle',
                parent=styles['Normal'],
                fontSize=9,
                textColor=brand_muted,
                spaceBefore=10,
            ),
        )
        elements.append(filter_paragraph)
    elements.append(Spacer(1, 16))

    elements.append(Paragraph("Detalle de reservas", section_title_style))

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
        ('BACKGROUND', (0, 0), (-1, 0), brand_primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#E5E7EB')),
        ('BOX', (0, 0), (-1, -1), 0.6, colors.HexColor('#D1D5DB')),
        ('LEFTPADDING', (0, 1), (-1, -1), 6),
        ('RIGHTPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    ])

    table = Table(data)
    for row_index in range(1, len(data)):
        background_color = colors.HexColor('#F7FBF9') if row_index % 2 else colors.white
        table_style.add('BACKGROUND', (0, row_index), (-1, row_index), background_color)

    table.setStyle(table_style)
    elements.append(table)
    if not queryset:
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("No se registran reservas para el rango seleccionado.", styles['Normal']))

    elements.append(Paragraph("Generado por Smart Spaces · Documento confidencial", footnote_style))

    # Construir el documento
    doc.build(elements)

    return response
