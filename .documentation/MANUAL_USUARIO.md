# Reservas Inteligentes – Manual de Usuario

Este documento describe la experiencia completa de la plataforma **Smart Spaces / Reservas Inteligentes**, diferenciando claramente lo que ve un **cliente** frente a un **administrador**.

---

## 1. Cómo empezar

### 1.1 Registro y acceso

- **Registro (`/register`)**: formulario con usuario (mínimo 3 caracteres), correo válido y contraseña con confirmación. Si todo está correcto se muestra el mensaje *“Cuenta creada correctamente…”* y se redirige automáticamente al inicio de sesión.

- **Inicio de sesión (`/login`)**: usuario y contraseña obligatorios. Al autenticarse se redirige a `/customer/welcome`. El token se guarda en `localStorage`, así que la sesión se mantiene entre recargas hasta que el usuario cierre sesión.

- **Cierre de sesión**: disponible en el menú del avatar (barra superior) y en el panel administrativo; elimina el token y regresa a `/login`.

### 1.2 Navegación compartida

- La barra superior (`app-navbar`) da acceso a **Explorar**, **Mis Reservas**, **Sobre nosotros** y **Contacto**.
- Al autenticarse se muestra un avatar con accesos directos a **Mi perfil**, **Panel administrativo** (solo roles `ADMIN`) y **Cerrar sesión**.

### 1.3 Roles

- **Cliente**: puede explorar espacios, revisar disponibilidad, reservar, gestionar sus reservas y editar su perfil.

- **Administrador**: además de lo anterior, puede entrar a `/admin` para operar espacios, tipos, descuentos, usuarios y reportes. El enlace aparece solo si el atributo `role` del usuario es `ADMIN`.

---

## 2. Portal de clientes (`/customer/...`)

### 2.1 Flujo típico de reserva

1. **Explorar espacios** (`/customer/spaces`), filtrar visualmente y abrir un espacio concreto.

2. **Detalle de espacio** (`/customer/space/:id`), elegir fecha en el calendario (no permite días pasados) y seleccionar franjas horarias contiguas. Al pulsar **Reservar ahora** se navega a la confirmación.

3. **Confirmación** (`/customer/booking-confirmation`), revisar resumen (fecha, horario, duración y total estimado) y finalizar con **Confirmar y pagar**. El componente llama a `BookingService.create` y redirige a **Mis Reservas**.

4. **Mis Reservas** (`/customer/my-bookings`), revisar estado de la nueva reserva y, si es necesario, cancelarla (POST `/bookings/{id}/cancel/`).

### 2.2 Páginas disponibles

#### Bienvenida – `/customer/welcome`

- Hero de marketing con los botones **Explorar Espacios** y **Iniciar sesión** (solo si no hay sesión).

#### Explorar espacios – `/customer/spaces`

- Listado cuadrícula alimentado por `SpaceService.list` con paginación (botones *Anterior/Siguiente*).
- Cada tarjeta incluye imagen dinámica (`https://placehold.co`), descripción y botón **Ver disponibilidad** que lleva al detalle del espacio.
- Mensajes de estado: *Cargando espacios...* y errores en `this.error`.

#### Detalle del espacio – `/customer/space/:id`

- Se carga la ficha mediante `SpaceService.get(id)`.
- **Calendario interactivo** (solo meses actuales/futuros). Los días pasados están deshabilitados (`isDayDisabled`).
- **Disponibilidad horaria**: `SpaceService.listAvailability(space.id, date)` devuelve franjas; el usuario debe elegir intervalos consecutivos. Si se rompe la secuencia aparece la advertencia *“Debes seleccionar horarios consecutivos…”*.
- **Resumen y precio**: muestra `price_per_hour` o “Precio no disponible”. También calcula fecha y horas seleccionadas.
- **Acciones**: `Reservar ahora` habilitado solo si hay fecha + hora de inicio y fin. El botón pasa la información por `router.navigate` hacia la confirmación.

#### Confirmación de reserva – `/customer/booking-confirmation`

- Requiere llegar desde el detalle; si se recarga sin `history.state` válido, redirige a `/customer/spaces`.
- Presenta resumen visual (imagen, fecha, horario, duración y total estimado). El costo se calcula con la tarifa base del tipo de servicio + precio por hora del espacio (`Space.service_type_detail`).
- Botones:
  - **Confirmar y pagar**: deshabilitado mientras `confirming` es `true`. Tras el POST exitoso a `/bookings/`, redirige a `/customer/my-bookings`.
  - **Cancelar**: regresa al detalle del espacio para modificar la selección.

#### Mis reservas – `/customer/my-bookings`

- Se alimenta con `BookingService.listForUser` separando **Próximas reservas** (`status: ACTIVE`) y **Historial** (`status: PAST`).
- Cada bloque tiene:
  - Estado de carga y error propios.
  - Paginación independiente (5 registros por página).
  - Botón **Cancelar** en las reservas activas (llama a `BookingService.cancel` y vuelve a cargar las listas).
  - En el historial se resalta si la reserva terminó *Completada* o *Cancelada* según `booking.status`.

#### Perfil – `/customer/profile` (protegido por `authGuard`)

- **Datos personales**: formulario editable con correo, nombres y apellidos.
  - Validación: el correo es obligatorio; si no hay cambios se informa *“No realizaste cambios”*.
  - Envío: `AuthService.updateProfile` y recarga del `BehaviorSubject`.
- **Bitácora de actividades**: tabla paginada (10 entradas) con filtros por método HTTP, código de estado, rango de fechas y texto (`/me/activity/`).
  - Muestra ruta, query params, IP y payload (si existe).
  - Botones **Aplicar filtros** y **Limpiar** reinician la consulta; controles de paginación usan `ActivityLogService.list`.

#### Sobre nosotros – `/customer/sobre-nosotros`

- Sección estática con misión, visión y motivos para elegir Smart Spaces. Incluye CTA a la página de contacto.

#### Contacto – `/customer/contacto`

- Presenta los canales oficiales (correo, teléfono, dirección, horario y redes).
- Formulario visual para nombre, correo y mensaje. El botón *Enviar mensaje* todavía no está ligado a un endpoint, por lo que funciona como recordatorio visual hasta que se conecte un backend.

---

## 3. Portal administrativo (`/admin`)

### 3.1 Shell del panel

- `DashboardComponent` crea el layout con barra lateral fija:
  - Accesos a **Panel de control (Reports)**, **Gestión de Espacios**, **Tipos de Espacio**, **Descuentos** y **Usuarios**.
  - Zona inferior con datos del usuario logueado y botones **Mi perfil** (regresa a `/customer/profile`) y **Cerrar sesión**.
- Todo el contenido principal se renderiza en el `<router-outlet>` central.

### 3.2 Reportes – `/admin/reports` (ruta por defecto)

- **Pestaña “Reservas actuales”** (estado `activeTab = 'current'`):
  - Tarjetas métricas (`ReportService.getMetrics`): total de reservas, horas, tasa de ocupación, reservas próximas e ingresos estimados.
  - Lista de reservas activas paginada (6 por página) obtenida vía `BookingService.listForUser`. Cada tarjeta incluye horario, descripción del espacio, cliente y valor final.
- **Pestaña “Historial de reservas”**:
  - Filtros para generar el PDF en línea (`ReportService.getBookingsPdf`): estado (todas/activas/completadas/canceladas) y rango de fechas.
  - Botones **Aplicar filtros**, **Limpiar** y **Actualizar PDF** regeneran el `Blob` y lo muestran en un `<iframe>`.
  - Estados visuales para carga o errores al obtener el archivo.

### 3.3 Gestión de espacios – `/admin/spaces`

- Tarjetas con nombre, descripción, tipo y tarifas.
- Botón **Nuevo espacio** abre un modal con formulario reactivo:
  - Campos: nombre (obligatorio), descripción y tipo de servicio (obligatorio).
  - Al guardar se elige automáticamente la primera página (creación) o se mantiene la actual (edición).
- Acciones por tarjeta:
  - **Editar**: precarga los datos en el formulario.
  - **Eliminar**: abre confirmación independiente.
- Paginación cuando `SpaceService.list` supera la página actual.
- Mensaje informativo si todavía no existen tipos de espacio (se requiere crearlos en el módulo siguiente).

### 3.4 Tipos de espacio – `/admin/space-types`

- Gestión similar a los espacios, pero centrada en las plantillas de servicio:
  - Campos: nombre, descripción, tarifa base, costo por hora y bandera *Disponible*.
  - Cada tarjeta muestra si el tipo está disponible o no (verde/rojo).
- Permite crear, editar y eliminar con confirmación modal.
- Es el prerrequisito para habilitar el formulario de nuevos espacios o descuentos.

### 3.5 Descuentos – `/admin/discounts`

- Lista de promociones asociadas a un tipo de espacio.
- Acciones:
  - **Añadir descuento**: abre modal con tipo, descripción, porcentaje y estado (activo por defecto).
  - **Editar**: reutiliza el modal con los valores existentes.
  - **Activar/Desactivar**: usa `DiscountService.toggle`.
  - **Eliminar**: solicita confirmación antes de llamar a `DiscountService.delete`.
- Indicadores muestran el porcentaje (chip) y el estado actual.
- Nota: si no existen tipos de espacio el botón se deshabilita y aparece un recordatorio.

### 3.6 Administración de usuarios – `/admin/users`

- Barra de búsqueda (por nombre o correo) que actualiza `UserAdminService.list` con el parámetro `search`.
- Tabla con correo, nombre calculado, rol y estado (chip verde/rojo). Las acciones disponibles por fila son:
  - **Cambiar estado** (toggle activo/inactivo).
  - **Eliminar** (con confirmación).
  - **Restablecer contraseña** (modal que exige una nueva contraseña de al menos 8 caracteres y llama a `reset-password`).
  - **Editar**: abre modal con datos bloqueados para usuario y correo pero permite cambiar nombre, rol, estado y contraseña opcional.
- Botón **Nuevo usuario**:
  - Habilita la edición de usuario/correo y exige contraseña mínima de 8 caracteres.
  - Campos disponibles: username, correo, nombres, rol (CLIENT/STAFF/MANAGER/ADMIN), activo, contraseña.
- Paginación centralizada (10 registros por página) y mensajes de carga/errores.

---

## 4. Buenas prácticas y notas finales

- **Consistencia de sesión**: al cambiar datos del perfil o del estado de un usuario, la UI espera respuesta del backend; permanece atento a los mensajes de error expuestos en cada formulario.
- **Prevención de datos huérfanos**: crea primero **Tipos de espacio** antes de intentar añadir espacios o descuentos para evitar formularios bloqueados.
- **Confirmación de reservas**: la página de confirmación depende del `state` del router; evita recargarla directamente para no perder los datos seleccionados.
- **Filtrado en actividad y reportes**: cuando los filtros no devuelven resultados se informa con estados vacíos; basta con limpiar filtros para volver a la vista general.
- **Formularios sin backend (Contacto)**: mientras no exista endpoint, usa los medios oficiales listados (correo, teléfono, WhatsApp) para contactar al equipo.
