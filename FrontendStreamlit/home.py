# main_app.py
import streamlit as st
import sys
import os

# Ajuste del PATH para importar módulos locales (como auth_logic y procesamiento)
# Asume que main_app.py y auth_logic.py están en la misma carpeta raíz.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Importar la lógica de autenticación y formularios desde auth_logic.py
from auth_logic import (
    init_session_state, 
    logout_user, 
    show_login_form, 
    show_register_form
)

# --- 1. CONFIGURACIÓN E INICIALIZACIÓN ---
st.set_page_config(layout="wide")
init_session_state() # Inicializa las variables de sesión: logged_in, access_token, etc.

st.title("Sistema de Gestión Logística con Django API")

# --- 2. FUNCIÓN PARA OCULTAR LA BARRA LATERAL NO AUTENTICADA ---
def hide_navigation():
    """Inyecta CSS para ocultar la barra de navegación lateral."""
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;} /* Oculta el menú hamburguesa */
            footer {visibility: hidden;} /* Oculta el footer (Made with Streamlit) */
            
            /* Oculta la barra de navegación multi-página */
            section[data-testid="stSidebarNav"] {
                display: none; 
            }
        </style>
    """, unsafe_allow_html=True)


# --- 3. RENDERIZADO CONDICIONAL (EL GESTOR DE VISTAS) ---

if st.session_state['logged_in']:
    # =========================================================
    # ESTADO: AUTENTICADO
    # =========================================================
    
    # Muestra el botón de logout en la barra lateral
    st.sidebar.title("Navegación")
    st.sidebar.success(f"Sesión activa: {st.session_state['username']}")
    
    if st.sidebar.button("Cerrar Sesión", key="logout_btn"):
        logout_user() # Limpia la sesión y fuerza la recarga (redirige al login)
        
    # Streamlit muestra automáticamente las páginas de la carpeta 'pages/' aquí.
    st.header("Bienvenido al Portal")
    st.info("Utiliza el menú lateral para acceder a la carga de datos y reportes.")

else:
    # =========================================================
    # ESTADO: NO AUTENTICADO (LOGIN/REGISTRO)
    # =========================================================
    
    hide_navigation() # Oculta la barra lateral para que no se vean los enlaces protegidos

    # Inicializa la variable para alternar entre Login y Registro
    if 'show_register' not in st.session_state:
        st.session_state['show_register'] = False
        
    st.markdown("---")
    
    # --- RENDERIZADO CONDICIONAL: REGISTRO vs LOGIN ---
    if st.session_state['show_register']:
        # Muestra el Formulario de Registro
        show_register_form()
        
        if st.button("Ya tengo cuenta, Iniciar Sesión"):
            st.session_state['show_register'] = False
            st.rerun()
            
    else:
        # Muestra el Formulario de Login
        show_login_form()
        
        if st.button("Crear una Cuenta"):
            st.session_state['show_register'] = True
            st.rerun()