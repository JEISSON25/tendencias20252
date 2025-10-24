import pandas as pd
from fpdf import FPDF  
from datetime import datetime

# -----------------------------------------------------------------------
# 🔹 Función: dibujar fila con ajuste de texto y altura uniforme (FINAL)
# -----------------------------------------------------------------------

def draw_table_row_with_multicell(pdf, data, col_widths, line_height=4.5):
    """
    Dibuja una fila de tabla con soporte para texto multilínea.
    Usa dry_run para calcular la altura máxima antes de dibujar.
    """
    
    # 1️⃣ Calcular la altura máxima requerida (dry_run)
    max_height = line_height
    x_start = pdf.get_x()
    y_start = pdf.get_y()
    
    for i, text in enumerate(data):
        width = col_widths[i]
        
        pdf.set_x(x_start + sum(col_widths[:i])) 
        
        # Simula la escritura
        pdf.multi_cell(width, line_height, text, border=0, align='L', dry_run=True) 
        
        current_cell_height = pdf.get_y() - y_start
        
        if current_cell_height > max_height:
            max_height = current_cell_height
            
        pdf.set_y(y_start)
        pdf.set_x(x_start) 

    # 2️⃣ Dibujar las celdas con la altura máxima
    pdf.set_xy(x_start, y_start) 

    for i, text in enumerate(data):
        width = col_widths[i]
        x_current = pdf.get_x()
        y_current = pdf.get_y()

        pdf.rect(x_current, y_current, width, max_height)
        
        # Dibuja la celda 
        pdf.multi_cell(width, line_height, text, border=0, align='L') 
        
        # Mover a la posición X correcta para la siguiente celda
        pdf.set_xy(x_current + width, y_current)

    # 3️⃣ Mover cursor a la siguiente fila
    pdf.set_xy(x_start, y_start + max_height)
    
    
# -----------------------------------------------------------------------
# 🔹 Función: generate_summary_pdf (CORREGIDA: Salida a bytes())
# -----------------------------------------------------------------------

def generate_summary_pdf(df: pd.DataFrame, data_dict: dict) -> bytes:
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # ... (código del encabezado y tabla) ...
    
    # Filas de datos
    pdf.set_font("Arial", '', 8)
    for _, row in df.iterrows():
        pdf.cell(40, 6, str(row.get("codigoZona", "")), 1, 0, 'L')
        pdf.cell(50, 6, str(row.get("identificacionAsociado", "")), 1, 0, 'L')
        pdf.cell(40, 6, str(row.get("origen", "")), 1, 0, 'L')
        pdf.cell(40, 6, f'{row.get("pesoUnitario", 0):.2f}', 1, 1, 'R')

    # 🛑 CORRECCIÓN FINAL: Conversión explícita a bytes()
    pdf_bytes = bytes(pdf.output(dest='S'))
    return pdf_bytes


# -----------------------------------------------------------------------
# 🔹 Función: generate_zonapeso_pdf (CORREGIDA: Salida a bytes())
# -----------------------------------------------------------------------

def generate_zonapeso_pdf(df: pd.DataFrame, data_dict: dict) -> bytes:
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ... (código del encabezado y tabla) ...

    col_widths = [28, 20, 42, 42, 25, 45, 25]
    headers = ["Ciudad", "Zona", "Asociado", "Vendedor", "Origen", "ID Odoo", "Peso Total (Kg)"]

    # Filas
    pdf.set_font("Arial", '', 8)
    for _, row in df.iterrows():
        row_data = [
            str(row.get("ciudad", row.get("cuidad", ""))),
            str(row.get("codigoZona", "")),
            str(row.get("nombreAsociado", "")),
            str(row.get("vendedor", "")),
            str(row.get("origen", "")),
            str(row.get("idOdoo", "")),
            f'{row.get("pesoUnitario", 0):.2f}'
        ]
        draw_table_row_with_multicell(pdf, row_data, col_widths, line_height=4.5)

 
    pdf_bytes = bytes(pdf.output(dest='S'))
    return pdf_bytes


# -----------------------------------------------------------------------
# 🔹 Función: generate_zonatotal_pdf (CORREGIDA: Anchos de columna y Salida a bytes())
# -----------------------------------------------------------------------

def generate_zonatotal_pdf(df: pd.DataFrame, data_dict: dict) -> bytes:
    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # ... (código del encabezado) ...

    # CORRECCIÓN DE ANCHOS
    col_widths = [30, 95, 20, 20, 20, 40, 40] 
    headers = ["Marca", "Producto", "Cant.", "Paca", "Unid.", "Origen", "Cód. Zona"]

    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", 'B', 8)
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 7, header, 1, 0, 'C', 1)
    pdf.ln()

    # Filas
    pdf.set_font("Arial", '', 8)
    for _, row in df.iterrows():
        row_data = [
            str(row.get("marca", "")),
            str(row.get("producto", "")),
            str(row.get("Unidades_pedidas", "")), 
            str(row.get("Pacas", "")),           
            str(row.get("Unidades_faltantes", "")), 
            str(row.get("Origen", "")),          
            str(row.get("Zona", ""))             
        ]
        draw_table_row_with_multicell(pdf, row_data, col_widths, line_height=4.5)

   
    pdf_bytes = bytes(pdf.output(dest='S'))
    return pdf_bytes


# -----------------------------------------------------------------------
# 🔹 Función: generate_bultostotal_pdf (CORREGIDA: Anchos de columna y Salida a bytes())
# -----------------------------------------------------------------------

