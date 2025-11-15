#!/bin/sh

echo "Aplicando migraciones..."
python manage.py migrate --noinput

echo "Creando superusuario si no existe..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="yojhan").exists():
    User.objects.create_superuser("yojhan", "yojhan@example.com", "cocoloco321")
EOF

echo "Iniciando Gunicorn..."
gunicorn grupo6_Ventas.wsgi:application --bind 0.0.0.0:8000
