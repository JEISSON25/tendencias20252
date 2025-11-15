from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



def generar_pdf_de_pedidos(pedidos):
    buf = BytesIO()
    hoja = canvas.Canvas(buf, pagesize=letter)
    ancho, alto = letter
    hoja.setFont("Times-Roman", 12)
    hoja.setTitle("Lista de Pedidos")
    y = alto - 50
    hoja.drawString(50, y, 'Lista de Pedidos:')
    y -= 40
    for pedido in pedidos:
        hoja.drawString(
            50, y -
            40, f'id pedido: {pedido.id}, direccion: {pedido.direccion}, estado: {pedido.estado}, '
            f' cliente: {pedido.cliente}')
        y -= 15

    hoja.showPage()
    hoja.save()
    buf.seek(0)
    return buf.getvalue()
