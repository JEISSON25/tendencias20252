# .devcontainer/Dockerfile
FROM python:3.10

# Evita la creación de archivos de byte-code de Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /workspace

# Instala dependencias del sistema operativo
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc

# Instala las dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000