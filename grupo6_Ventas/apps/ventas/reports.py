# apps/ventas/reports.py
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def ventas_pdf(ventas_queryset):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50

    p.setFont("Helvetica-Bold", 14)
    p.drawString(40, y, "Reporte de Ventas")
    y -= 30
    p.setFont("Helvetica", 10)

    total_general = 0.0
    for v in ventas_queryset:
        line = f"#{v.id} | Cliente: {getattr(v.cliente, 'nombre', '')} | Fecha: {v.fecha:%Y-%m-%d} | Total: {v.total}"
        p.drawString(40, y, line)
        y -= 15
        total_general += float(v.total or 0)
        if y < 50:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 10)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y - 10, f"TOTAL GENERAL: {total_general}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.getvalue()
