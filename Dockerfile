FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

WORKDIR /app/grupo6_Ventas

# Primero migramos 
RUN python manage.py migrate --noinput

# Crear superusuario automáticamente
RUN echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
User.objects.filter(username='yojhan').exists() or \
User.objects.create_superuser('yojhan','yojhan@example.com','cocoloco321')" \
| python manage.py shell

CMD ["gunicorn", "grupo6_Ventas.wsgi:application", "--bind", "0.0.0.0:8000"]
