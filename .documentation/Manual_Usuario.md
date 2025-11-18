
Manual de Usuario
Sistema de Gestión de Inventarios (Farmacia)

Versión 1.0 – Aplicación Backend (API REST)

1. Introducción

El Sistema de Gestión de Inventarios para Farmacia es una plataforma web diseñada para administrar:

Productos y categorías

Proveedores y clientes

Inventario y movimientos

Empleados

Facturación y detalles de venta

Reportes PDF

Este manual está dirigido a administradores, empleados, proveedores y clientes.
Aquí aprenderás:

Cómo iniciar sesión

Cómo usar cada módulo

Cómo generar reportes

Qué permisos tiene tu rol

2. Perfiles de Usuario y Permisos
Rol	Permisos
Administrador	Control total del sistema
Empleado	Gestión de inventario, ventas y clientes
Cliente	Consultar sus datos
Proveedor	Consultar y mantener su información
3. Ingreso al Sistema (Autenticación JWT)
3.1 Obtener Token de Acceso

Enviar usuario y contraseña válidos.

Endpoint:
POST /api/token/

Ejemplo de solicitud:

{
  "username": "admin",
  "password": "adminpass123"
}


Respuesta:

{
  "access": "token_de_acceso",
  "refresh": "token_de_refresco"
}

3.2 Usar el Token

Todos los módulos protegidos requieren:

Authorization: Bearer <access_token>

4. Módulo de Categorías
4.1 Consultar Categorías

GET /api/categorias/

4.2 Crear Categoría (solo administrador)

POST /api/categorias/

Ejemplo:

{
  "nombre": "Antibióticos"
}

4.3 Editar Categoría

PATCH /api/categorias/{id}/

4.4 Eliminar Categoría

DELETE /api/categorias/{id}/

5. Módulo de Productos
5.1 Consultar Productos

GET /api/productos/

5.2 Registrar Producto

POST /api/productos/

{
  "nombre": "Ibuprofeno",
  "precio": 15.75,
  "stock": 50,
  "id_categoria": 1,
  "id_proveedor": 3
}

5.3 Editar Producto

PATCH /api/productos/{id}/

5.4 Eliminar Producto

DELETE /api/productos/{id}/

5.5 Generar PDF

Producto individual:
GET /api/productos/{id}/pdf/

Todos los productos:
GET /api/productos/all_pdf/

6. Módulo de Proveedores
6.1 Consultar Proveedores

GET /api/proveedores/

6.2 Registrar Proveedor

POST /api/proveedores/

{
  "nombre": "Droguería Central",
  "contacto": "drogueria@example.com",
  "usuario": 8
}

6.3 Editar Proveedor

PATCH /api/proveedores/{id}/

6.4 Eliminar Proveedor

DELETE /api/proveedores/{id}/

7. Módulo de Clientes
7.1 Consultar Clientes

GET /api/clientes/

7.2 Registrar Cliente

POST /api/clientes/

7.3 Editar Cliente

PATCH /api/clientes/{id}/

7.4 Eliminar Cliente

DELETE /api/clientes/{id}/

8. Módulo de Empleados
8.1 Consultar Empleados

GET /api/empleados/

8.2 Registrar Empleado

POST /api/empleados/

8.3 Editar Empleado

PATCH /api/empleados/{id}/

8.4 Eliminar Empleado

DELETE /api/empleados/{id}/

9. Módulo de Facturación
9.1 Crear Factura

POST /api/facturasventa/

{
  "id_cliente": 10,
  "id_empleado": 5
}

9.2 Consultar Facturas

GET /api/facturasventa/

10. Módulo de Detalles de Venta
10.1 Crear Detalle

POST /api/detallesventa/

10.2 Consultar Detalles

GET /api/detallesventa/

10.3 Editar Detalle

PATCH /api/detallesventa/{id}/

10.4 Eliminar Detalle

DELETE /api/detallesventa/{id}/

10.5 PDFs

Detalle individual: /api/detallesventa/{id}/pdf/

Todos los detalles: /api/detallesventa/all_pdf/

11. Módulo de Movimientos de Inventario
11.1 Consultar Movimientos

GET /api/movimientos/

11.2 Registrar Movimiento

POST /api/movimientos/

{
  "tipo": "entrada",
  "cantidad": 10,
  "id_producto": 4,
  "id_cliente": 2
}

11.3 Editar Movimiento

PATCH /api/movimientos/{id}/

11.4 Eliminar Movimiento

DELETE /api/movimientos/{id}/

11.5 PDFs

Movimiento individual: /api/movimientos/{id}/pdf/

Todos los movimientos: /api/movimientos/all_pdf/

12. Herramientas Adicionales
12.1 Pruebas Automáticas

Incluye pruebas de:

Autenticación

Permisos

CRUD

Generación de PDF

Flujo completo

Ejecutar:

pytest

12.2 Swagger UI

Permite probar la API desde el navegador.
Acceso:

/swagger/

13. Resolución de Problemas Comunes
Problema	Solución
401 Unauthorized	No se envió el token o está vencido
403 Forbidden	El rol no tiene permisos suficientes
500 Internal Server Error	Revisar el formato o datos enviados
PDF vacío o corrupto	Verificar que el registro exista correctamente