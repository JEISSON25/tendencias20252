import streamlit as st
import numpy as np
import pandas as pd
import requests
from urllib.parse import urlencode
from datetime import datetime, timedelta
# Importa tus funciones de autenticación
from auth_logic import protected_get, protected_patch, DJANGO_API_BASE, logout_user 

# --- CONFIGURACIÓN Y CONSTANTES ---

API_URL = DJANGO_API_BASE + "procesamiento/reporte_datos/"
API_PATCH_URL = DJANGO_API_BASE + "procesamiento/actualizar_picking_masivo/"

DEFAULT_START_DATE = datetime.now().date() - timedelta(days=30)
DEFAULT_END_DATE = datetime.now().date()

# --- VERIFICACIÓN DE SESIÓN ---

if not st.session_state.get('logged_in'):
    st.error("🔒 Debe iniciar sesión para acceder a esta página.")
    st.stop()

# --- INICIALIZACIÓN DE ESTADO ---

if 'report_data' not in st.session_state:
    st.session_state['report_data'] = pd.DataFrame()
if 'run_query' not in st.session_state:
    st.session_state['run_query'] = False

# --------------------------------------------------------------------------
# --- FUNCIONES DE LÓGICA DE DATOS ---
# --------------------------------------------------------------------------
def convert_to_native_types(data):
    """Convierte los tipos NumPy a tipos nativos de Python para la serialización JSON."""
    
    # 1. Manejo de tipos complejos (Listas y Diccionarios)
    if isinstance(data, dict):
        # Recursión en diccionarios
        return {k: convert_to_native_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        # Recursión en listas
        return [convert_to_native_types(item) for item in data]
    
    # 2. Manejo de Valores Nulos (pd.NaT, np.nan, None)
    elif pd.isna(data):
        return None
    
    # 3. Manejo de Tipos Numéricos de NumPy
    elif isinstance(data, (np.integer, np.int64)):
        return int(data)
    elif isinstance(data, (np.floating, np.float64)):
        return float(data)
    
    # 4. Manejo de Tipos de Fecha de NumPy
    elif isinstance(data, np.datetime64):
        # Convertir a cadena de texto ISO para serialización
        return str(data) 

    # 5. Si no es un tipo especial, devolver el dato original
    return data



def fetch_filtered_data(fecha_inicio, fecha_fin, origen):
    """Realiza la petición GET protegida con filtros dinámicos."""
    params = {}
    
  
    params["date_start"] = fecha_inicio.isoformat()
    params["date_end"] = fecha_fin.isoformat()
    
    if origen:
         params["origen"] = origen
           
    query_string = urlencode(params)
    full_url = f"{API_URL}?{query_string}"
    
    response = protected_get(full_url)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        st.error("❌ Sesión expirada. Por favor, inicie sesión de nuevo.")
        logout_user()
        return None
    else: 
        st.error(f"Error al cargar datos: Código {response.status_code}.")
        try:
            st.code(response.json())
        except:
            st.code(response.text)
        return None


def send_patch_request(original_df, changes):
    
    # 1. Crear la lista de cambios
    patch_data = []
    
    # El diccionario 'edited_rows' contiene los cambios por índice de fila
    for index_str, changed_values in changes['edited_rows'].items():
        
        index = int(index_str)
        
       
        # Utilizamos .iloc para acceder a la fila por índice entero
        registro_pk = original_df.iloc[index]['id'] 
        registro_pk = int(registro_pk)
        
        
        
        # Construir el payload con el ID y solo los campos editados
        payload = {"id": registro_pk} 
        converted_changes = convert_to_native_types(changed_values)
        
        payload.update(converted_changes)
        
        # Añadir al lote
        patch_data.append(payload) 


    # 2. Enviar la petición PATCH masiva
    with st.spinner("Enviando actualización a Django..."):
        response = protected_patch(API_PATCH_URL, data=patch_data) 
        
        if response.status_code == 200:
            st.success("🎉 ¡Datos actualizados con éxito! Recargando datos...")
            st.session_state['run_query'] = True 
            st.rerun() 
        else:
            st.error(f"❌ Error al aplicar PATCH: Código {response.status_code}")
            try:
                st.json(response.json())
            except:
                st.code(response.text)

# --------------------------------------------------------------------------
# --- COMPONENTE DE VISUALIZACIÓN Y EDICIÓN ---
# --------------------------------------------------------------------------

def display_data_editor(df_data: pd.DataFrame):
    st.subheader("Modificar Datos ")
    
    # Muestra el editor y guarda los cambios en st.session_state['data_editor']
    edited_df = st.data_editor(
        df_data,
        key="data_editor",
        use_container_width=True,
        hide_index=True,
        # Define los campos clave que no pueden ser modificados
        disabled=("id",)
    )
    
    changes = st.session_state["data_editor"]
    
    # ✅ El botón de guardado debe estar aquí, después del st.data_editor
    if st.button("Guardar Cambios Editados", type="primary"):
        
        if changes.get('edited_rows'):
            send_patch_request(df_data, changes)
        else:
            st.info("No se detectaron celdas modificadas para guardar.")

# --------------------------------------------------------------------------
# --- PÁGINA PRINCIPAL ---
# --------------------------------------------------------------------------

def reporte_page():
    st.title("📋 Consulta de Datos por Rango de Fechas y Edición")
    
    # --- WIDGETS DE FILTRO ---
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        fecha_inicio = st.date_input("Fecha de Inicio ", DEFAULT_START_DATE)
    
    with col2:
        fecha_fin = st.date_input("Fecha de Fin ", DEFAULT_END_DATE)
    
    with col3:
        origen = st.text_input("Origen")
        
    with col4:
        st.markdown("<br>", unsafe_allow_html=True) 
        if st.button("Aplicar Filtros y Consultar", type="primary"):
            st.session_state['run_query'] = True 
            st.rerun() 
            
    # --- LÓGICA DE CONSULTA ---
    if st.session_state['run_query']:
        
        st.session_state['run_query'] = False
        
        if fecha_inicio > fecha_fin:
            st.warning("⚠️ La fecha de inicio no puede ser posterior a la fecha de fin.")
            st.session_state['report_data'] = pd.DataFrame()
        else:
            with st.spinner("Consultando datos en Django..."):
                data_json = fetch_filtered_data(fecha_inicio, fecha_fin, origen)
                
                if data_json is None:
                    st.session_state['report_data'] = pd.DataFrame()
                elif not data_json:
                    st.warning("No se encontraron registros para el rango de fechas seleccionado.")
                    st.session_state['report_data'] = pd.DataFrame()
                else:
                    df_reporte = pd.DataFrame(data_json)
                    st.session_state['report_data'] = df_reporte
                    st.success(f"Consulta exitosa. Se encontraron {len(df_reporte)} registros.")


    # --- VISUALIZACIÓN DEL EDITOR ---
    # Mostramos el editor si tenemos datos.
    if not st.session_state['report_data'].empty:
        display_data_editor(st.session_state['report_data'])
        
def main():
    st.set_page_config(layout="wide")
    st.title("📊 Modelo de datos")
    st.header("En esta sección podras modificar los datos importados al sistema")
    reporte_page()
    
if __name__ == '__main__':
    main()