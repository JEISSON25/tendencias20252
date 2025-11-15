FROM python:3.11-slim

# Evita el buffering de python
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar requerimientos
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar TODO el proyecto
COPY . /app/

# Entrar al directorio donde está manage.py
WORKDIR /app/grupo6_Ventas

# Crear superusuario automáticamente (solo si no existe)
RUN echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='yojhan').exists() or \
User.objects.create_superuser('yojhan','yojhan@example.com','cocoloco321')" \
| python manage.py shell

# Ejecutar gunicorn usando el wsgi correcto
CMD ["gunicorn", "grupo6_Ventas.wsgi:application", "--bind", "0.0.0.0:8000"]
