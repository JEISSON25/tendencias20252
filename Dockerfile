FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

WORKDIR /app/grupo6_Ventas

# Ejecutamos todo desde el entrypoint
CMD ["sh", "entrypoint.sh"]
