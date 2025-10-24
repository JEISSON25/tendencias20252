# auth_logic.py
import streamlit as st
import requests

# URL de tus endpoints de autenticación (basado en la estructura que definimos)
DJANGO_API_BASE = "http://127.0.0.1:8000/api/"
LOGIN_URL = DJANGO_API_BASE + "auth/jwt/create/" 
REFRESH_URL = DJANGO_API_BASE + "auth/jwt/refresh/"
DJANGO_REGISTER_URL = DJANGO_API_BASE + "register/users/"


# --- GESTIÓN DE LA SESIÓN ---

def init_session_state():
    """Inicializa todas las variables de sesión necesarias."""
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['access_token'] = None
        st.session_state['refresh_token'] = None
        st.session_state['username'] = None

def logout_user():
    """Limpia el estado de la sesión para cerrar la sesión."""
    # (Opcional: puedes añadir aquí la llamada a /jwt/blacklist/ con el refresh token)
    st.session_state['logged_in'] = False
    st.session_state['access_token'] = None
    st.session_state['refresh_token'] = None
    st.session_state['username'] = None
    st.rerun()

# --- FORMULARIO Y LÓGICA DE LOGIN ---

def login_user(username, password):
    """Llama a la API de Django para obtener tokens."""
    try:
        response = requests.post(LOGIN_URL, json={"username": username, "password": password})
        
        if response.status_code == 200:
            tokens = response.json()
            
            # Guardar tokens y estado
            st.session_state['access_token'] = tokens['access']
            st.session_state['refresh_token'] = tokens['refresh']
            st.session_state['username'] = username
            st.session_state['logged_in'] = True
            st.success(f"Bienvenido, {username}!")
            st.rerun()
            return True
        else:
            st.error("Credenciales inválidas.")
            return False
    except requests.exceptions.ConnectionError:
        st.error("Error de conexión. Revisa que tu servidor de Django esté corriendo.")
        return False

# --- FUNCIÓN CENTRAL DE PETICIÓN PROTEGIDA ---

def get_auth_headers():
    """Retorna los encabezados con el Access Token."""
    token = st.session_state.get('access_token')
    if token:
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    return {"Content-Type": "application/json"}

def protected_post(url, data):
    headers = get_auth_headers()
    return requests.post(url, json=data, headers=headers)


def show_login_form():
    """Renderiza y maneja el formulario de inicio de sesión."""
    st.header("🔐 Iniciar Sesión")
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            with st.spinner("Autenticando..."):
                login_user(username, password)
                
                
def register_user(username, email, password, re_password):
    """Llama a la API de Django para registrar un nuevo usuario."""
    data = {
        "username": username,
        "email": email,
        "password": password,
        "re_password": re_password
    }
    try:
        response = requests.post(DJANGO_REGISTER_URL, json=data)
        
        if response.status_code == 201:
            st.success("¡Registro exitoso! Por favor, inicia sesión.")
            return True
        else:
            st.error("Error en el registro.")
            st.json(response.json()) # Mostrar errores de validación de Django
            return False
    except requests.exceptions.ConnectionError:
        st.error("Error de conexión con el backend de Django.")
        return False

def show_register_form():
    """Renderiza el formulario de registro."""
    st.header("✨ Crear Nueva Cuenta")
    with st.form("register_form"):
        username = st.text_input("Usuario (Registro)")
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")
        re_password = st.text_input("Repetir Contraseña", type="password")
        submitted = st.form_submit_button("Registrarse")

        if submitted:
            with st.spinner("Creando cuenta..."):
                if register_user(username, email, password, re_password):
                    # Tras el registro exitoso, volver al login
                    st.session_state['show_register'] = False
                    st.rerun()