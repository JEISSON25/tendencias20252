# procesamiento/utilformatos.py
import pandas as pd
from xhtml2pdf import pisa
from io import BytesIO
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

# --- CONFIGURACIÓN DE RUTAS ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Inicializamos Jinja2 con la función de autoescape importada
JINJA_ENV = Environment(
    loader=FileSystemLoader(CURRENT_DIR),
    autoescape=select_autoescape(['html']) # <-- Ahora está definido
)
LISTADO_TEMPLATE_FILE = 'listado_total_table.html'


def render_to_pdf(html_content: str) -> bytes:
    """Convierte una cadena HTML en un archivo PDF binario (bytes)."""
    
    result_file = BytesIO()

    # La función pisa.pisaDocument hace la conversión
    pisa_status = pisa.pisaDocument(
        src=BytesIO(html_content.encode("utf-8")), 
        dest=result_file                              
    )

    if not pisa_status.err:
        return result_file.getvalue()
    
    # Manejo de error si la generación falla
    print(f"XHTML2PDF ERROR: {pisa_status.err}")
    return None # Retornamos None si hay un error

def transformacion_pdf_listado(df_listado: pd.DataFrame, datos_clave: dict = None) -> bytes:
    """
    Convierte el DataFrame de Listado Total en un PDF binario.
    """
    
    # 1. Conversión de DataFrame a HTML
    right_aligned_cols = [
        'Unidades_pedidas', 
        'Pacas', 
        'Unidades_faltantes'
    ]
    
    # Creamos un diccionario de formatters para añadir la clase CSS de alineación
    formatters = {col: lambda x: f'<span class="align-right">{x}</span>' for col in right_aligned_cols}

    df_html = df_listado.to_html(
        index=False,
        classes="data-table", 
        formatters=formatters,
        escape=False 
    )

    # 2. Renderizar la Plantilla Jinja2
    
    template = JINJA_ENV.get_template(LISTADO_TEMPLATE_FILE)
    
    final_html = template.render(
        report_table_html=df_html,
        datos_clave=datos_clave 
    )

    
    return render_to_pdf(final_html)