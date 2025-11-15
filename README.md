# Reservas Inteligentes

Plataforma modular para gestionar reservas y disponibilidades de espacios, construida con Django y desplegable tanto de forma local como en entornos remotos.

## Tabla de contenido

- [Enlaces importantes](#enlaces-importantes)
- [Requisitos previos](#requisitos-previos)
- [Ejecución con Docker](#ejecución-con-docker)
- [Uso con Dev Containers](#uso-con-dev-containers)
- [Recursos adicionales](#recursos-adicionales)

## Enlaces importantes

- **Frontend en producción:** [https://gentle-beach-0e664550f.3.azurestaticapps.net](https://gentle-beach-0e664550f.3.azurestaticapps.net)

- **Manual de usuario:** `.documentation/MANUAL_USUARIO.md`

## Requisitos previos

- Docker y Docker Compose instalados.
- VS Code con la extensión **Dev Containers** (opcional, solo si quieres desarrollar dentro de un contenedor).
- Variables de entorno configuradas: copia `.documentation/.env.example` a `.env` en la raíz y ajusta credenciales sensibles (sobre todo Maileroo y PostgreSQL).

## Ejecución con Docker

1. Construye y levanta los servicios:

   ```bash
   docker compose up --build
   ```

2. Docker creará dos contenedores:
   - `app`: ejecuta el backend Django en `http://localhost:8000`.
   - `db`: base de datos PostgreSQL con persistencia en `postgres_data`.

3. Las migraciones se aplican de forma automática antes de arrancar el servidor (ver comando en `docker-compose.yml`).

4. Para detener los servicios:

   ```bash
   docker compose down
   ```

## Uso con Dev Containers

1. Abre el proyecto en VS Code.
2. Instala la extensión **Dev Containers** si aún no lo has hecho.
3. Usa `Dev Containers: Reopen in Container` desde la paleta de comandos. VS Code utilizará `.devcontainer/devcontainer.json`, que referencia el mismo `docker-compose.yml`.
4. Una vez dentro del contenedor, utiliza los comandos de Django (por ejemplo, `python manage.py runserver 0.0.0.0:8000`) o lanza servicios auxiliares según necesites.
5. Los puertos expuestos (por defecto 8000) se reenvían automáticamente a tu máquina local.

## Recursos adicionales

- `docker-compose.yml`: orquestación de los servicios `app` y `db`.
- `.devcontainer/`: configuración para entornos reproducibles con VS Code.
- `smartreservations/`, `bookings/`, `users/`: módulos Django principales.
- `.documentation/MANUAL_USUARIO.md`: guía funcional dirigida a usuarios finales.
- `.documentation/.env.example`: plantilla de variables de entorno sin datos sensibles.
