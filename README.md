LINK Del BACK: https://prueba-de-despliegue-wyj1.onrender.com
LINK DEL FRONTEND : https://frontend-inventory-farmacia.netlify.app

Documentación de la API – Sistema de Gestión de Inventarios (Farmacia)

API REST desarrollada en Django + Django REST Framework para gestionar inventarios, productos, movimientos, ventas, usuarios y reportes PDF.
Incluye autenticación JWT y control de acceso por roles.

1. Información General

Tecnologías:

Django 5

Django REST Framework

Base de datos: SQLite / PostgreSQL

Autenticación: JSON Web Tokens (JWT)

Reportes PDF: ReportLab

Versionado: API v1

Documentación: Swagger UI / Redoc

Rutas de documentación:

URL	Descripción
/swagger/	Documentación Swagger UI
/redoc/	Documentación Redoc
/swagger.yaml	Esquema OpenAPI
2. Autenticación JWT
Obtener Tokens

POST /api/token/

Body:

{
  "username": "admin",
  "password": "adminpass123"
}


Response:

{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}

Refrescar Token

POST /api/token/refresh/

{
  "refresh": "jwt_refresh_token"
}

3. Roles y Permisos
Rol	Permisos principales
Administrador	CRUD completo
Empleado	Ventas, movimientos, clientes
Cliente	Consultar su información
Proveedor	Gestión de productos propios (si aplica)

Todos los endpoints protegidos requieren:

Authorization: Bearer <access_token>

4. Módulos y Endpoints
4.1 Usuarios

Listar usuarios
GET /api/usuario/

Crear usuario
POST /api/usuario/

{
  "username": "newuser",
  "email": "new@example.com",
  "password": "NewPass123!",
  "telefono": "3001112222",
  "rol": 3
}


Obtener usuario por ID
GET /api/usuario/{id}/

Actualizar usuario
PATCH /api/usuario/{id}/

Eliminar usuario
DELETE /api/usuario/{id}/

4.2 Categorías

Listar categorías
GET /api/categorias/

Crear categoría
POST /api/categorias/

{
  "nombre": "Vitaminas"
}


Obtener categoría
GET /api/categorias/{id}/

Actualizar categoría
PATCH /api/categorias/{id}/

Eliminar categoría
DELETE /api/categorias/{id}/

4.3 Proveedores

Listar proveedores
GET /api/proveedores/

Crear proveedor
POST /api/proveedores/

{
  "nombre": "Proveedor Test",
  "contacto": "proveedor@test.com",
  "usuario": 1
}


Obtener proveedor
GET /api/proveedores/{id}/

4.4 Productos

Listar productos
GET /api/productos/

Crear producto
POST /api/productos/

{
  "nombre": "Ibuprofeno",
  "precio": 15.75,
  "stock": 50,
  "id_categoria": 2,
  "id_proveedor": 3
}


Obtener producto
GET /api/productos/{id}/

Actualizar producto
PATCH /api/productos/{id}/

Eliminar producto
DELETE /api/productos/{id}/

PDFs de productos
Endpoint	Descripción
/api/productos/{id}/pdf/	PDF individual
/api/productos/all_pdf/	PDF general de productos
4.5 Clientes

Listar clientes
GET /api/clientes/

Crear cliente
POST /api/clientes/

Obtener cliente
GET /api/clientes/{id}/

4.6 Empleados

Rutas estándar REST:

GET /api/empleados/
POST /api/empleados/
PATCH /api/empleados/{id}/
DELETE /api/empleados/{id}/

4.7 Facturas de Venta

Crear factura

{
  "id_cliente": 7,
  "id_empleado": 8
}


Rutas:

/api/facturasventa/
/api/facturasventa/{id}/

4.8 Detalles de Venta

Crear detalle

{
  "cantidad": 3,
  "precio_unitario": 12.00,
  "id_factura": 15,
  "id_producto": 10
}


Rutas:

/api/detallesventa/
/api/detallesventa/{id}/


PDFs

/api/detallesventa/{id}/pdf/

/api/detallesventa/all_pdf/

4.9 Movimientos de Inventario

Crear movimiento

{
  "tipo": "entrada",
  "cantidad": 10,
  "id_producto": 10,
  "id_cliente": 7
}


Listar movimientos
GET /api/movimientos/

Obtener movimiento
GET /api/movimientos/{id}/

PDFs

Endpoint	Descripción
/api/movimientos/{id}/pdf/	PDF individual
/api/movimientos/all_pdf/	PDF general
5. Errores Comunes
Código	Descripción
400	Datos inválidos
401	Falta token JWT
403	Sin permisos
404	No encontrado
500	Error interno del servidor
6. Autenticación en Swagger

Abrir la opción Authorize.

Ingresar el token como:

Bearer <access_token>


Confirmar.

7. Arquitectura General

Patrón MVC + DRF ViewSets

Serializers para conversión Modelo ↔ JSON

Permisos personalizados según rol

Pruebas automatizadas (pytest / APITestCase)

Generación de reportes PDF

Logging y manejo centralizado de errores

Si deseas, puedo:

Darte versión más resumida

Convertirlo en OpenAPI YAML real

Crear un README.md completo para tu repositorio

Diseñar un diagrama de arquitectura