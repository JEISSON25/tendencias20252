# # Grupo 6 - API Django (Productos/Clientes)

## Pasos
python -m venv entorno
entorno\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver

## Endpoints
GET/POST    /api/productos/
GET/PUT/DEL /api/productos/<id>/
GET/POST    /api/clientes/
GET/PUT/DEL /api/clientes/<id>/
