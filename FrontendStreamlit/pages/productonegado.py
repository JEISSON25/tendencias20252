
import sys
import os
# Agrega la carpeta padre (FrontendStreamlit) al PATH.
# Esto permite que Python encuentre el paquete 'procesamiento'.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#Libreria
import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from io import BytesIO
#FUNCIONES PROPIAS
from procesamiento.utils import convert_dates_to_iso
from procesamiento.utilexport import rutaPesodf, listadoTotal, BultosMasivo, Regerospickingmasivo, RegerosSeleccion
from FrontendStreamlit.procesamiento.html.utilsformatoshtml import transformacion_pdf_listado
#FUNCIONES DE AUTENTICACIÓN
from auth_logic import protected_post, logout_user, DJANGO_API_BASE


# Constante que usaremos como placeholder en lugar de NaN para la serialización

NAN_PLACEHOLDER = "__NAN_PLACEHOLDER__"

API_URL = DJANGO_API_BASE + "procesamiento/upload_picking_packing/"

#La libreria streamlit requiere  de la libreria io para generar los formatos de texto
if not st.session_state.get('logged_in'):
    st.error("🔒 Debe iniciar sesión para acceder a esta página.")
    # El CSS oculta el enlace, pero este código impide que el contenido se cargue
    st.stop()

def to_excel(df):

    """Convierte el DataFrame a un archivo Excel binario."""

    output = BytesIO()

    # Requiere el paquete openpyxl o xlsxwriter

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:

        df.to_excel(writer, index=False, sheet_name='Resumen_Negados')

    processed_data = output.getvalue()

    return processed_data



def display_summary_report():

    if not st.session_state['latest_summary'].empty:

        st.header("Información del corte")

        st.markdown("Resumen de la información")

       

        df_summary = st.session_state['latest_summary']

       

        col_vis, col_down = st.columns([3, 1])

        with col_vis:

            st.dataframe(df_summary, use_container_width=True, hide_index=True)



        with col_down: 
    # --- 1. BOTÓN DE EXCEL ---# 
          excel_data = to_excel(df_summary) 
          st.download_button( 
                    label="Descargar Resumen a Excel", 
                    data=excel_data, file_name='resumen_picking_packing.xlsx', 
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                    help='Descarga el resumen del picking y packing.' 
                    ) 
    # --- 2. PREPARAR DATOS CLAVE PARA EL PDF --- # Si el DF de resumen no está vacío, usamos la primera fila como referencia datos_clave = { "nombre_cliente": df_summary['nombreAsociado'].iloc[0] if 'nombreAsociado' in df_summary.columns else "Cliente Desconocido", "id_documento": "CARGA-" + pd.Timestamp.now().strftime("%Y%m%d%H%M"), # ID de carga único "vendedor": df_summary['vendedor'].iloc[0] if 'vendedor' in df_summary.columns else "N/A", "ciudad": df_summary['cuidad'].iloc[0] if 'cuidad' in df_summary.columns else "N/A", "codigo_zona": df_summary['codigoZona'].iloc[0] if 'codigoZona' in df_summary.columns else "N/A", "zona": df_summary['zona'].iloc[0] if 'zona' in df_summary.columns else "N/A", } # --- 3. BOTÓN DE PDF --- # Genera el PDF usando la función externa y el DataFrame de resumen pdf_data = generate_summary_pdf(df_summary, datos_clave) if pdf_data: st.download_button( label="Descargar Resumen a PDF", data=pdf_data, file_name='resumen_picking_packing.pdf', mime='application/pdf', help='Descarga el resumen del picking y packing en PDF.' ) # --- 3. BOTÓN DE RUTA ZONA PESO --- dfzonapeso = rutaPesodf(df_summary) pdfzonapeso = generate_zonapeso_pdf(dfzonapeso, datos_clave) if pdfzonapeso: st.download_button( label="Descargar Pesos por Zona a PDF", data=pdfzonapeso, file_name='resumen_zona_peso.pdf', mime='application/pdf', help='Descarga el resumen del zona peso en PDF.' )
    # Si el DF de resumen no está vacío, usamos la primera fila como referencia
          datos_clave = { "nombre_cliente": df_summary['nombreAsociado'].iloc[0] if 
                        'nombreAsociado' in df_summary.columns else "Cliente Desconocido", 
                        "id_documento": "CARGA-" + pd.Timestamp.now().strftime("%Y%m%d%H%M"), 
                        "vendedor": df_summary['vendedor'].iloc[0] if 'vendedor' in df_summary.columns else "N/A", 
                        "ciudad": df_summary['cuidad'].iloc[0] if 'cuidad' in df_summary.columns else "N/A", 
                        "codigo_zona": df_summary['codigoZona'].iloc[0] if 'codigoZona' in df_summary.columns else "N/A", 
                        "zona": df_summary['zona'].iloc[0] if 'zona' in df_summary.columns else "N/A"
                        }
    # --- 3. BOTÓN DE PDF --- #
    # Genera el PDF usando la función externa y el DataFrame de resumen
          pdf_data = generate_summary_pdf(df_summary, datos_clave)
          if pdf_data: st.download_button( 
                    label="Descargar Resumen a PDF", 
                    data=pdf_data, file_name='resumen_picking_packing.pdf', 
                    mime='application/pdf', 
                    help='Descarga el resumen del picking y packing en PDF.' 
                    )
    # --- 3. BOTÓN DE RUTA ZONA PESO ---
          dfzonapeso = rutaPesodf(df_summary)
          pdfzonapeso = generate_zonapeso_pdf(dfzonapeso, datos_clave)
          if pdfzonapeso: st.download_button( 
                     label="Descargar Pesos por Zona a PDF", 
                     data=pdfzonapeso, 
                     file_name='resumen_zona_peso.pdf', 
                     mime='application/pdf', 
                     help='Descarga el resumen del zona peso en PDF.' 
                     )
    # --- 4. BOTÓN DE LISTADO TOTAL ---
          dflistadototal = listadoTotal(df_summary)
          pdflistadototal = transformacion_pdf_listado(dflistadototal, datos_clave)
          if pdflistadototal: st.download_button( 
                     label="Descargar listado total a PDF", 
                     data=pdflistadototal, 
                     file_name='listado_total.pdf', 
                     mime='application/pdf', 
                     help='Descarga el resumen del listado total en PDF.' 
                     )
      
# ----------------------------------------------------------------------

#Esta función es para guardar datos y no se pierda en los otros procesos

if 'latest_summary' not in st.session_state:

    st.session_state['latest_summary'] = pd.DataFrame()

   

def main():

  st.set_page_config(layout="wide")

  st.title("📊 Carga y Reporte de corte de Selección y empaque")

  st.header("1. Ingresar las facturas en borrador")

  st.subheader("Recuerda que debes exportar la plantilla pick multy")

  st.caption("el archivo plno no debe contener titulos, verifica que no los tenga")


  #Carga de datos
  uploaded_file = st.file_uploader("Cargar archivo XLSX", type=["xlsx"])

  if uploaded_file:
    # 1. Lectura y preparación para envío
    df_original = pd.read_excel(uploaded_file)
    #Las bases de datos estandarizan la forma de utilizar los formatos fecha
    df_para_envio = convert_dates_to_iso(df_original.copy())
    # Reemplazo de NaN por placeholder para la serialización (mi archivo plano tiene nulos que proceso en el backend)
    df_para_envio = df_para_envio.replace({np.nan: NAN_PLACEHOLDER})
    #Transformaciones de datos para su uso
    data_to_send = df_para_envio.to_dict(orient='records')

    if st.button("Procesar Picking y Packing", type="primary"):
     with st.spinner("Generando reportes ...."):
        try:
            response = protected_post(API_URL, data=data_to_send)
            
            
            if response.status_code == 401:
                st.error("❌ Sesión expirada o no autorizada. Por favor, inicie sesión de nuevo.")
                logout_user() 
                return
            
            
            try:
                response_data = response.json()
            except requests.exceptions.JSONDecodeError:
                st.error(f"❌ Error API: El servidor devolvió una respuesta no válida ({response.status_code}).")
                st.code(response.text) 
                return

          
            if response.status_code == 201:
                st.success(f"✅ Datos guardados. Filas: {response_data.get('filas_guardadas')}")
                summary_data = response_data.get('resumen_procesado', [])
                
                if summary_data:
                    df_summary = pd.DataFrame(summary_data)
                    st.session_state['latest_summary'] = df_summary
                    st.toast("Resumen de carga generado.")
                    pass

            elif response.status_code == 400:
                st.error("❌ Error de validación en Django. Verifique los detalles.")
                st.json(response_data)

            else:
                
                st.error(f"❌ Error API: {response.status_code}")
              
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Error de conexión. Revisa el servidor.")
            
    display_summary_report()



if __name__ == '__main__':

    main()