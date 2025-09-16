# Multy-Project: Sistema de Gestión Logística

Sistema web desarrollado con **Django** y **Django REST Framework** para la gestión integral de productos, facturas, asociados, y la automatización de procesos logísticos.

---

## 📋 Funcionalidades

- Gestión de Productos: referencias, nombres, marcas, precios.  
- Control de Inventario: registro de productos pedidos y productos negados.  
- Registro de Transacciones: manejo de facturación que relaciona productos, asociados, vendedores y conductores.  
- API RESTful para interactuar con los datos del sistema.  
- Documentación automática de la API mediante Swagger/OpenAPI (usando DRF Spectacular).

---

## 🛠 Tecnologías

- Python 3.13  
- Django 5.2.6  
- Django REST Framework  
- DRF Spectacular para la documentación de la API  

---

## ⚙️ Instalación y puesta en marcha

Sigue estos pasos para correr el proyecto en tu máquina local.

```bash
# Clona el repositorio
git clone https://github.com/scubillosj/multy-project.git
cd multy-project

# Crea un entorno virtual (recomendado)
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS / Linux
source venv/bin/activate

# Instala dependencias
pip install -r requirements.txt

# Realiza migraciones
python manage.py migrate

# Crea un superusuario (opcional, para acceder al admin)
python manage.py createsuperuser

# Corre el servidor localmente
python manage.py runserver
