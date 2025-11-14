# Usar Python 3.11 (compatible con psycopg2)
FROM python:3.11-slim

# Evitar buffer de logs
ENV PYTHONUNBUFFERED=1

# Crear directorio
WORKDIR /app

# Copiar requirements
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar todo el proyecto
COPY . /app/

# Exponer puerto
EXPOSE 8000

# Comando para correr Django
CMD ["gunicorn", "grupo6_Ventas.grupo6_Ventas.wsgi:application", "--bind", "0.0.0.0:8000"]

