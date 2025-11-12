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
import plotly.express as px
from io import BytesIO
#FUNCIONES PROPIAS
from procesamiento.utils import convert_dates_to_iso, limpiar_y_preparar_detalle
from procesamiento.html.utilsformatoshtml import productonegado_pdf
#FUNCIONES DE AUTENTICACIÓN
from auth_logic import protected_post, logout_user, DJANGO_API_BASE
# Constante que usaremos como placeholder en lugar de NaN para la serialización

NAN_PLACEHOLDER = "__NAN_PLACEHOLDER__"

API_URL = DJANGO_API_BASE + "procesamiento/upload_producto_negado/"

if not st.session_state.get('logged_in'):
    st.error("🔒 Debe iniciar sesión para acceder a esta página.")
    st.stop()


def to_excel(df):
    """Convierte el DataFrame a un archivo Excel binario."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Resumen_Negados')
    processed_data = output.getvalue()
    return processed_data


def display_summary_report():
    
    # ✅ Lógica de Gráfico y Display MOVIDA dentro del IF
    if not st.session_state['latest_summary'].empty:
        st.header("Producto negado")
        st.markdown("Resumen de la información")

        df_summary = st.session_state['latest_summary']
        
        # 1. Agrupación
        df_agrupado = df_summary.groupby('marca').size().reset_index(name='cantidad_negada')
    
        # 2. Crear el Gráfico Circular con Plotly Express (AHORA DENTRO DEL IF)
        fig = px.pie(
            df_agrupado,
            values='cantidad_negada',
            names='marca',
            title='Distribución de Unidades negadas por Marca',
            hover_data=['cantidad_negada'], 
            labels={'cantidad_negada': 'Total Unidades'}
        )
        
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+value', 
            hovertemplate='Marca: %{label}<br>Unidades: %{value}<br>Porcentaje: %{percent}<extra></extra>'
        )
        
        # 3. Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
        # 4. Mostrar la tabla de resumen (opcional)
        st.subheader("Datos Agrupados")
        st.dataframe(df_agrupado, use_container_width=True, hide_index=True)

#Esta función es para guardar datos y no se pierda en los otros procesos
if 'latest_summary' not in st.session_state:
    st.session_state['latest_summary'] = pd.DataFrame()


def main():

    st.set_page_config(layout="wide")
    st.title("📊 Carga y Reporte de producto negado")
    st.header("1. Ingresar las ordenes a procesar")
    st.subheader("Recuerda que debes exportar la Pyhon-Producto negado")
    st.caption("el archivo no debe contener titulos ni agrupaciones, verificar que no los tenga")


    #Carga de datos
    uploaded_file = st.file_uploader("Cargar archivo XLSX", type=["xlsx"])

    if uploaded_file:
        # 1. Lectura y preparación para envío
        df_original = pd.read_excel(uploaded_file)
        df_para_envio = convert_dates_to_iso(df_original.copy())
        
        # Transformación de datos 
        df_productonegado = limpiar_y_preparar_detalle(df_para_envio.copy())
        df_pn_visualizacion = df_productonegado.groupby(["fecha","marca", "producto"])[
         ["cantidad_negada","origen", "referencia"]].agg(
               cantidad_negada=("cantidad_negada", "sum"),
               origen=("origen", lambda x: ", ".join(x.unique())),
               referencia=("referencia", lambda x: ", ".join(x.unique()))).reset_index()
        
        # ----------------------------------------------------
        # BLOQUE DE VISUALIZACIÓN PREVIA Y BOTÓN DE PDF
        # ----------------------------------------------------
        
        col_vis, col_down = st.columns([3, 1])

        with col_vis:
            st.dataframe(df_pn_visualizacion, use_container_width=True, hide_index=True)
            
        with col_down: 
            # ✅ Preparar datos clave para el PDF (Usando el DF limpio)
            datos_clave = { 
                "nombre_cliente": df_productonegado['nombreAsociado'].iloc[0] if 'nombreAsociado' in df_productonegado.columns else "Cliente Desconocido", 
                "id_documento": "CARGA-" + pd.Timestamp.now().strftime("%Y%m%d%H%M"), 
                "vendedor": df_productonegado['vendedor'].iloc[0] if 'vendedor' in df_productonegado.columns else "N/A", 
                "ciudad": df_productonegado['cuidad'].iloc[0] if 'cuidad' in df_productonegado.columns else "N/A", 
                "codigo_zona": df_productonegado['codigoZona'].iloc[0] if 'codigoZona' in df_productonegado.columns else "N/A", 
                "zona": df_productonegado['zona'].iloc[0] if 'zona' in df_productonegado.columns else "N/A", 
            }
            
            # Botón de PDF 
            pdf_data = productonegado_pdf(df_pn_visualizacion, datos_clave)
            if pdf_data: 
                st.download_button( 
                    label="Descargar Resumen a PDF", 
                    data=pdf_data,
                    file_name='resumen_productonegado.pdf',
                    mime='application/pdf', 
                    help='Descarga el resumen del producto negado'
                )
        
        # ----------------------------------------------------
        
   
        data_to_send = df_productonegado.to_dict(orient='records')

        if st.button("Procesar Producto negado", type="primary"):
            with st.spinner("Generando reportes ...."):
                try:
                    response = protected_post(API_URL, data=data_to_send)
                    
                    if response is None:
                      st.error("❌ No se obtuvo respuesta del servidor. Verifica la conexión o el endpoint.")
                      st.session_state['latest_summary'] = pd.DataFrame()
                      return
                     
                    if response.status_code == 401:
                        st.error("❌ Sesión expirada o no autorizada. Por favor, inicie sesión de nuevo.")
                        logout_user() 
                        return
                    
                    response_data = response.json()
                    
                    if response.status_code == 201:
                        st.success(f"✅ Datos guardados. Filas: {response_data.get('filas_guardadas')}")
                        summary_data = response_data.get('resumen_procesado', [])
                        
                        if summary_data:
                            df_summary_result = pd.DataFrame(summary_data)
                            # ✅ ALMACENAR DATOS FINALES PARA VISUALIZACIÓN
                            st.session_state['latest_summary'] = df_summary_result
                            st.toast("Resumen de carga generado.")
                            st.rerun() # Forzar rerun para mostrar el gráfico

                    elif response.status_code == 400:
                        st.error("❌ Error de validación en Django. Verifique los detalles.")
                        st.json(response_data)

                    else:
                        st.error(f"❌ Error API: {response.status_code}")
                        st.code(response.text)
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Error de conexión. Revisa el servidor.")
                except requests.exceptions.JSONDecodeError:
                    st.error(f"❌ Error API: El servidor devolvió una respuesta no válida ({response.status_code}).")
                    st.code(response.text)

    display_summary_report()


if __name__ == '__main__':
    main()