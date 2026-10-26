# Cine Paradiso: product backlog

| | |
|---|---|
| **Materia** | Introducción al Desarrollo de Software, FIUBA (Cátedra Lanzillotta, 2.º cuatrimestre 2026) |
| **Entrega** | Hito 1 (26/10/2026) |
| **Fuentes** | [Enunciado oficial](Proyecto%20integrador%20IDS%202026.pdf) · [`alcance-y-supuestos.md`](alcance-y-supuestos.md) · [`endpoints.md`](endpoints.md) · [`Tablas.sql`](Tablas.sql) · [`Mockups.pdf`](Mockups.pdf) (19 pantallas; la referencia "M-n" indica la página n) |

## Índice

1. [Convenciones](#1-convenciones)
2. [Resumen del backlog](#2-resumen-del-backlog)
3. [Historias de usuario por módulo](#3-historias-de-usuario-por-módulo)
4. [Trazabilidad con los requisitos obligatorios](#4-trazabilidad-con-los-requisitos-obligatorios)


---

## 1. Convenciones

### 1.1 Formato de las historias

Cada historia tiene un identificador (`PB-XX`), el enunciado *"Como [rol], quiero [funcionalidad], para [beneficio]"*, criterios de aceptación verificables, prioridad, estimación y dependencias. Las referencias `S1`–`S25` remiten a `alcance-y-supuestos.md`, y las rutas, a `endpoints.md`.

### 1.2 Roles

| Rol | Descripción |
|---|---|
| **Visitante** | Persona que navega el sitio sin sesión iniciada. |
| **Cliente** | Usuario registrado con rol cliente. |
| **Administrador** | Usuario con rol administrador (Backoffice). |
| **Equipo** | Integrantes del equipo de desarrollo (historias técnicas y de proceso que exige el enunciado). |

### 1.3 Prioridad

| Prioridad | Criterio |
|---|---|
| **Alta** | Requisito obligatorio del enunciado, o base técnica sin la cual no se puede cumplir uno. |
| **Media** | Funcionalidad que surge de los endpoints o los mockups acordados por el equipo, pero que el enunciado no pide de forma explícita. |
| **Baja** | Funcionalidad deseable (no obligatoria). Queda fuera del alcance inicial (sección 3 de `alcance-y-supuestos.md`). |

### 1.4 Estimación

como medida relativa de esfuerzo y complejidad puntuamos las tareas de 1-10 

---

## 2. Resumen del backlog

Las historias están ordenadas por módulo, siguiendo las dependencias. Dentro de cada módulo, primero van las de mayor prioridad.

| ID | Módulo | Historia (resumen) | Prioridad | SP | Depende de |
|---|---|---|---|---|---|
| PB-01 | Base técnica | Repositorio GitHub y estrategia de ramas | Alta | 2 | — |
| PB-02 | Base técnica | Tablero Kanban con el backlog | Alta | 1 | PB-01 |
| PB-03 | Base técnica | Script SQL de creación y carga | Alta | 3 | PB-01 |
| PB-04 | Base técnica | Backend Flask base con conexión a MySQL | Alta | 5 | PB-03 |
| PB-05 | Base técnica | Frontend y Backoffice Flask base, con layout responsive | Alta | 5 | PB-04 |
| PB-06 | Usuarios | Registro de clientes | Alta | 3 | PB-05 |
| PB-07 | Usuarios | Inicio y cierre de sesión | Alta | 3 | PB-06 |
| PB-08 | Usuarios | Seguridad de los endpoints por rol | Alta | 5 | PB-07 |
| PB-09 | Usuarios | Gestión de usuarios por el administrador | Media | 3 | PB-08 |
| PB-10 | Usuarios | Edición de los datos propios | Media | 2 | PB-08 |
| PB-11 | Películas | Búsqueda e importación de películas desde TMDB | Alta | 8 | PB-08 |
| PB-12 | Películas | Listado, edición y baja de películas | Alta | 5 | PB-11 |
| PB-13 | Salas y funciones | Consulta de locales, salas y capacidades | Alta | 2 | PB-04 |
| PB-14 | Salas y funciones | Alta de funciones con validación de reglas | Alta | 8 | PB-12, PB-13 |
| PB-15 | Salas y funciones | Listado, modificación y baja de funciones | Alta | 5 | PB-14 |
| PB-16 | Salas y funciones | Vista semanal de programación | Media | 3 | PB-15 |
| PB-17 | Cartelera | Cartelera pública con filtros | Alta | 5 | PB-14 |
| PB-18 | Servicios | ABM de servicios adicionales | Alta | 3 | PB-08 |
| PB-19 | Cartelera | Detalle de película con sus funciones | Alta | 3 | PB-17 |
| PB-20 | Compras | Mapa de butacas de una función | Alta | 5 | PB-19 |
| PB-21 | Compras | Checkout de entradas y servicios con pago simulado | Alta | 8 | PB-18, PB-20 |
| PB-22 | Compras | Generación de QR y envío del comprobante por email | Alta | 8 | PB-21 |
| PB-23 | Compras | Cancelación de una compra | Alta | 5 | PB-22 |
| PB-24 | Perfil | Historial de compras y consumos | Alta | 5 | PB-21 |
| PB-25 | Validación QR | Validación del QR en el ingreso a la sala | Alta | 8 | PB-22 |
| PB-26 | Perfil | Películas vistas | Alta | 2 | PB-24, PB-25 |
| PB-27 | Dashboards | Ocupación por función y por película | Alta | 5 | PB-21 |
| PB-28 | Dashboards | Ventas por género | Alta | 3 | PB-21 |
| PB-29 | Dashboards | Franjas horarias más vendidas | Alta | 3 | PB-21 |
| PB-30 | Dashboards | Cancelaciones | Alta | 3 | PB-23 |
| PB-31 | Dashboards | Resumen general con indicadores | Media | 3 | PB-27 a PB-30 |
| PB-32 | Entrega | `init.sh` e instrucciones de ejecución | Alta | 2 | PB-05 |
| PB-33 | Entrega | Informe final del proyecto | Alta | 3 | — |
| PB-34 | Deseables | Reporte PDF de ventas | Baja | 5 | PB-27 |
| PB-35 | Deseables | Reseñas y puntuación de películas | Baja | 5 | PB-26 |
| PB-36 | Deseables | Documentación de la API con Swagger | Baja | 3 | PB-04 |
| PB-37 | Deseables | Dockerización del proyecto | Baja | 3 | PB-32 |
| PB-38 | Deseables | Despliegue en servicios gratuitos | Baja | 5 | PB-37 |

**Totales propuestos:**

| Prioridad | Historias | Story Points |
|---|---|---|
| Alta | 29 | 126 |
| Media | 4 | 11 |
| Baja | 5 | 21 |
| **Total** | **38** | **158** |

---

## 3. Historias de usuario por módulo

### 3.1 Base técnica

#### PB-01 · Repositorio GitHub y estrategia de ramas

**Historia:** Como integrante del equipo, quiero un repositorio en GitHub con una estrategia de ramas definida, para trabajar en paralelo sin pisar el trabajo de los demás.

**Criterios de aceptación**

- [ ] Existe un repositorio en GitHub, compartido con el corrector de la cátedra.
- [ ] Todos los integrantes tienen acceso de escritura.
- [ ] La rama principal está protegida y los cambios entran mediante *pull requests* desde ramas de trabajo.
- [ ] La estrategia de ramas y la convención de mensajes de commit (asociados a una tarea del tablero) están documentadas en el `README`.
- [ ] La carpeta `docs/` con la documentación del Hito 1 está subida al repositorio.

**Prioridad:** Alta · **Estimación:** 2 SP · **Depende de:** —

#### PB-02 · Tablero Kanban con el backlog

**Historia:** Como integrante del equipo, quiero un tablero Kanban con el backlog de producto, para organizar y repartir las tareas de forma equitativa.

**Criterios de aceptación**

- [ ] Hay un tablero en GitHub Projects, Trello o Jira, con columnas que reflejan el flujo de trabajo (por ejemplo: Backlog, Por hacer, En curso, En revisión, Hecho).
- [ ] Todas las historias de este documento están cargadas en el tablero.
- [ ] Cada tarea en curso tiene un responsable asignado.

**Prioridad:** Alta · **Estimación:** 1 SP · **Depende de:** PB-01

#### PB-03 · Script SQL de creación y carga

**Historia:** Como integrante del equipo, quiero un script SQL que cree la base de datos y cargue los datos iniciales, para que cualquiera pueda levantar el entorno igual.

**Criterios de aceptación**

- [ ] El script crea la base `cine_paradiso` en MySQL 8.0.16 o superior, con todas las tablas del esquema (`Tablas.sql`).
- [ ] Precarga los 3 locales, sus salas, todas las butacas, los géneros y la cuenta del administrador (S6, S21).
- [ ] Toda fecha con hora se guarda en un único campo `DATETIME`.
- [ ] El script se ejecuta sin errores sobre una instalación limpia de MySQL.

**Prioridad:** Alta · **Estimación:** 3 SP · **Depende de:** PB-01

#### PB-04 · Backend Flask base con conexión a MySQL

**Historia:** Como integrante del equipo, quiero una aplicación backend en Flask que se conecte a MySQL, para construir sobre ella todos los endpoints de la API.

**Criterios de aceptación**

- [ ] El backend se conecta a MySQL usando sentencias SQL explícitas, sin ORM ni clases que mapeen tablas.
- [ ] Al abrir cada conexión se fija la zona horaria de Argentina (S24).
- [ ] Los pedidos y las respuestas usan JSON.
- [ ] Los errores responden con el código HTTP y el formato definidos en las secciones 1.5 y 1.6 de `endpoints.md`.
- [ ] La configuración (credenciales, claves de API) se toma de variables de entorno o de un archivo excluido del repositorio, no de variables globales del código.

**Prioridad:** Alta · **Estimación:** 5 SP · **Depende de:** PB-03

#### PB-05 · Frontend y Backoffice Flask base, con layout responsive

**Historia:** Como visitante, quiero que el sitio se vea bien en la computadora, la tablet y el celular, para poder usarlo desde cualquier dispositivo.

**Criterios de aceptación**

- [ ] El frontend y el Backoffice son aplicaciones Flask con plantillas Jinja2, HTML, CSS y Bootstrap (S25).
- [ ] Se comunican con el backend solo desde Python, con la librería `requests`. No hay `fetch`, `axios`, `XMLHttpRequest` ni equivalentes en el navegador.
- [ ] Existe un layout común para el front (encabezado con "Cartelera" y "Mi perfil") y otro para el Backoffice (menú lateral), según los mockups.
- [ ] Las páginas se adaptan sin desplazamiento horizontal a anchos de celular, tablet y escritorio.
- [ ] Si el backend no responde o devuelve un error, se muestra un mensaje comprensible y la aplicación no se rompe.

**Prioridad:** Alta · **Estimación:** 5 SP · **Depende de:** PB-04

### 3.2 Usuarios y autenticación

#### PB-06 · Registro de clientes

**Historia:** Como visitante, quiero registrarme con mi nombre, correo y contraseña, para poder comprar entradas.

**Criterios de aceptación**

- [ ] El formulario pide nombre, correo electrónico y contraseña (S20).
- [ ] Si el correo ya está registrado, se informa el error y no se crea la cuenta (`409`).
- [ ] Si faltan datos o el formato del correo es inválido, se informa el error (`400`).
- [ ] La contraseña se guarda con un hash seguro, nunca en texto plano.
- [ ] La cuenta creada tiene siempre el rol cliente; no es posible registrarse como administrador (S21).

**Prioridad:** Alta · **Estimación:** 3 SP · **Depende de:** PB-05 · **Endpoint:** `POST /auth/registro`

#### PB-07 · Inicio y cierre de sesión

**Historia:** Como cliente o administrador, quiero iniciar y cerrar sesión, para acceder a las funciones de mi rol.

**Criterios de aceptación**

- [ ] Con credenciales correctas, se inicia la sesión y el token se guarda en la sesión de Flask.
- [ ] Con credenciales incorrectas, se muestra un error sin indicar cuál de los dos datos falló (`401`).
- [ ] Un usuario dado de baja no puede iniciar sesión (`403`).
- [ ] Después del login, el cliente va al front y el administrador, al Backoffice.
- [ ] Al cerrar sesión ("Salir"), el token se borra y las páginas protegidas dejan de ser accesibles.

**Prioridad:** Alta · **Estimación:** 3 SP · **Depende de:** PB-06 · **Endpoint:** `POST /auth/login`

#### PB-08 · Seguridad de los endpoints por rol

**Historia:** Como administrador, quiero que cada endpoint verifique la identidad y el rol de quien lo usa, para que nadie acceda a datos u operaciones que no le corresponden.

**Criterios de aceptación**

- [ ] Todo endpoint que no sea público rechaza los pedidos sin token o con token inválido (`401`).
- [ ] Los endpoints de rol Admin rechazan a los clientes (`403`).
- [ ] Los endpoints de rol Dueño rechazan a un cliente que no hizo la compra (`403`).
- [ ] Las páginas del Backoffice redirigen al login si no hay sesión de administrador.
- [ ] El mecanismo cumple lo que responda el tutor sobre "seguridad en todos los endpoints" (T6).

**Prioridad:** Alta · **Estimación:** 5 SP · **Depende de:** PB-07

#### PB-09 · Gestión de usuarios por el administrador

**Historia:** Como administrador, quiero listar usuarios, ver su detalle, cambiarles el rol o darlos de baja, para mantener el control de las cuentas del sistema.

**Criterios de aceptación**

- [ ] El listado permite buscar por nombre o correo y filtrar por rol y estado.
- [ ] El detalle muestra los datos del usuario y su cantidad de compras.
- [ ] El administrador puede cambiar el rol o dar de baja a un usuario (baja lógica); un rol inválido se rechaza (`422`).
- [ ] Un usuario dado de baja no puede iniciar sesión y su historial de compras se conserva.

**Prioridad:** Media · **Estimación:** 3 SP · **Depende de:** PB-08 · **Endpoints:** `GET /usuarios`, `GET /usuarios/{id}`, `PATCH /usuarios/{id}`

#### PB-10 · Edición de los datos propios

**Historia:** Como usuario registrado, quiero modificar mi nombre y mi contraseña, para mantener mis datos actualizados.

**Criterios de aceptación**

- [ ] Se puede cambiar el nombre.
- [ ] Para cambiar la contraseña hay que ingresar la actual; si es incorrecta, se rechaza el cambio (`401`).
- [ ] La nueva contraseña se guarda con un hash seguro.

**Prioridad:** Media · **Estimación:** 2 SP · **Depende de:** PB-08 · **Endpoints:** `GET /usuarios/me`, `PATCH /usuarios/me`

### 3.3 Películas (Backoffice)

#### PB-11 · Búsqueda e importación de películas desde TMDB

**Historia:** Como administrador, quiero buscar películas en TMDB e importarlas con su período de cartelera, para cargar el catálogo sin escribir los datos a mano.

**Criterios de aceptación**

- [ ] Desde "Gestión de películas" → "Importar TMDB", se busca por texto y se ven título, año, sinopsis y póster en español (S9).
- [ ] Las películas ya importadas aparecen marcadas y no se pueden importar dos veces (`409`).
- [ ] Al importar, el administrador elige la clasificación (ATP, +13, +16, +18) y el período de cartelera (desde/hasta) (S9, S10).
- [ ] Se guardan en MySQL el título, la sinopsis, el póster, la duración y los géneros obtenidos de TMDB (S8).
- [ ] Si la fecha de fin es anterior a la de inicio, se rechaza (`422`).
- [ ] Si TMDB no responde, se muestra un mensaje de error y el sistema sigue funcionando (`502`).

**Prioridad:** Alta · **Estimación:** 8 SP · **Depende de:** PB-08 · **Endpoints:** `GET /tmdb/peliculas`, `POST /peliculas`

#### PB-12 · Listado, edición y baja de películas

**Historia:** Como administrador, quiero ver, editar y dar de baja las películas importadas, para mantener la cartelera actualizada.

**Criterios de aceptación**

- [ ] El listado muestra póster, título, géneros, clasificación, período de cartelera y estado ("En cartelera" o "Próximamente").
- [ ] Se puede buscar por título y filtrar por género, clasificación y estado.
- [ ] Se pueden editar la sinopsis, el póster, la clasificación y el período de cartelera (S8, S9, S10).
- [ ] No se puede acortar el período si deja funciones ya programadas fuera de él (`422`).
- [ ] La baja es lógica: la película deja de aparecer en la cartelera y se conservan las compras y estadísticas.
- [ ] No se puede dar de baja una película con funciones futuras activas (`409`).

**Prioridad:** Alta · **Estimación:** 5 SP · **Depende de:** PB-11 · **Endpoints:** `GET /peliculas`, `GET /peliculas/{id}`, `PATCH /peliculas/{id}`, `DELETE /peliculas/{id}`

### 3.4 Salas y funciones

#### PB-13 · Consulta de locales, salas y capacidades

**Historia:** Como visitante, quiero conocer los locales, sus salas y la capacidad de cada una, para elegir dónde ver una película.

**Criterios de aceptación**

- [ ] Se listan los 3 locales con sus salas, la cantidad de filas y columnas y la capacidad de cada sala.
- [ ] Los datos provienen de la precarga en MySQL; no hay ABM de locales ni salas (S6).

**Prioridad:** Alta · **Estimación:** 2 SP · **Depende de:** PB-04 · **Endpoint:** `GET /locales`

#### PB-14 · Alta de funciones con validación de reglas

**Historia:** Como administrador, quiero crear funciones indicando película, sala, fecha y hora y precio, para programar la cartelera de cada sala.

**Criterios de aceptación**

- [ ] El formulario "Nueva función" pide película, local/sala, fecha y hora (un único `DATETIME`) y precio (S4, S11).
- [ ] Se rechaza una función fuera del período de cartelera de la película o en el pasado (`422`).
- [ ] Se rechaza una función que se superpone con otra de la misma sala, considerando la duración de la película y 20 minutos de limpieza (S12, `422`).
- [ ] Se rechaza un precio menor o igual a cero.
- [ ] La función creada queda visible en la gestión de funciones y en la cartelera.

**Prioridad:** Alta · **Estimación:** 8 SP · **Depende de:** PB-12, PB-13 · **Endpoint:** `POST /funciones`

#### PB-15 · Listado, modificación y baja de funciones

**Historia:** Como administrador, quiero listar, modificar y dar de baja funciones, para corregir la programación cuando haga falta.

**Criterios de aceptación**

- [ ] El listado se puede filtrar por película, local, sala y fecha, y permite incluir funciones pasadas o dadas de baja.
- [ ] Se puede cambiar la sala, la fecha y hora o el precio de una función sin compras activas; se vuelven a validar las reglas de S12.
- [ ] No se puede modificar ni dar de baja una función con compras activas (`409`).
- [ ] La baja es lógica.

**Prioridad:** Alta · **Estimación:** 5 SP · **Depende de:** PB-14 · **Endpoints:** `GET /funciones`, `GET /funciones/{id}`, `PATCH /funciones/{id}`, `DELETE /funciones/{id}`

#### PB-16 · Vista semanal de programación

**Historia:** Como administrador, quiero ver las funciones de una semana organizadas por día, para detectar huecos o cargas excesivas en la programación.

**Criterios de aceptación**

- [ ] La pantalla "Horarios y programación" muestra una columna por día con las funciones (película, hora y sala).
- [ ] Se puede elegir la semana y filtrar por local ("Todos" por defecto).
- [ ] Se puede navegar a la semana anterior y a la siguiente.

**Prioridad:** Media · **Estimación:** 3 SP · **Depende de:** PB-15 · **Endpoints:** `GET /funciones?desde=...&hasta=...`, `GET /locales` · **Mockup:** M-15

### 3.5 Cartelera y servicios

#### PB-17 · Cartelera pública con filtros

**Historia:** Como visitante, quiero ver las películas en cartel y filtrarlas por fecha, local y género, para encontrar rápido qué ver.

**Criterios de aceptación**

- [ ] Se muestran las películas activas, con su período de cartelera vigente y al menos una función futura.
- [ ] Cada tarjeta muestra póster, título, género y el botón "Ver funciones".
- [ ] Se puede filtrar por fecha (hoy por defecto), local y género.
- [ ] La cartelera se lee de MySQL, aunque TMDB no esté disponible (S8).

**Prioridad:** Alta · **Estimación:** 5 SP · **Depende de:** PB-14 · **Endpoint:** `GET /cartelera`

#### PB-18 · ABM de servicios adicionales

**Historia:** Como administrador, quiero cargar, modificar y dar de baja servicios adicionales, para ofrecer comida, bebidas, estacionamiento o acceso VIP junto con las entradas.

**Criterios de aceptación**

- [ ] Se puede crear un servicio con nombre, descripción y precio; un precio negativo se rechaza (`422`).
- [ ] Se puede modificar el nombre, la descripción y el precio, y reactivar un servicio dado de baja.
- [ ] La baja es lógica: el servicio deja de ofrecerse en nuevas compras.
- [ ] Los servicios están disponibles para todas las salas y no tienen control de stock (S5).
- [ ] Las compras anteriores conservan el precio que tenían al momento de comprar.

**Prioridad:** Alta · **Estimación:** 3 SP · **Depende de:** PB-08 · **Endpoints:** `GET /servicios`, `POST /servicios`, `PATCH /servicios/{id}`, `DELETE /servicios/{id}`

#### PB-19 · Detalle de película con sus funciones

**Historia:** Como visitante, quiero ver el detalle de una película con sus funciones disponibles, para elegir a qué función ir.

**Criterios de aceptación**

- [ ] El detalle muestra sinopsis, póster, duración, clasificación y géneros.
- [ ] Se listan las funciones futuras de la película con local, sala, fecha y hora, precio y butacas libres.
- [ ] Al elegir una función se pasa a la selección de butacas (flujo película → función → butacas).
- [ ] Si la película no existe o fue dada de baja, se muestra un mensaje adecuado (`404`).

**Prioridad:** Alta · **Estimación:** 3 SP · **Depende de:** PB-17 · **Endpoints:** `GET /peliculas/{id}`, `GET /funciones?pelicula_id={id}`

### 3.6 Compras

#### PB-20 · Mapa de butacas de una función

**Historia:** Como cliente, quiero ver el mapa de la sala con las butacas libres y ocupadas, para elegir dónde sentarme.

**Criterios de aceptación**

- [ ] Se muestra una grilla con la pantalla arriba, filas identificadas con letras y columnas con números (S7).
- [ ] Las butacas ocupadas, libres y seleccionadas se distinguen visualmente.
- [ ] Una butaca de una compra cancelada aparece como libre.
- [ ] No se pueden seleccionar butacas ocupadas ni más de 6 butacas (S3).
- [ ] La selección funciona sin JavaScript que haga pedidos (formulario HTML enviado a Flask).

**Prioridad:** Alta · **Estimación:** 5 SP · **Depende de:** PB-19 · **Endpoints:** `GET /funciones/{id}`, `GET /funciones/{id}/butacas`

#### PB-21 · Checkout de entradas y servicios con pago simulado

**Historia:** Como cliente, quiero confirmar la compra de mis entradas y, si quiero, agregar servicios, para asegurar mi lugar en la función.

**Criterios de aceptación**

- [ ] Hay que tener la sesión iniciada como cliente para confirmar.
- [ ] El resumen muestra la función, las butacas, los servicios elegidos con su cantidad y el total en ARS (S24).
- [ ] La compra incluye entre 1 y 6 entradas de una sola función (S3); fuera de ese rango se rechaza (`422`).
- [ ] El pago es simulado: al confirmar, la compra queda en estado `confirmada` (S1).
- [ ] Si otra persona compró alguna de las butacas antes, la compra se rechaza completa, se informa cuál está ocupada y no se registra nada (`409`, S23).
- [ ] No se pueden comprar entradas para funciones pasadas o dadas de baja, ni servicios inactivos (`422`).

**Prioridad:** Alta · **Estimación:** 8 SP · **Depende de:** PB-18, PB-20 · **Endpoint:** `POST /compras`

#### PB-22 · Generación de QR y envío del comprobante por email

**Historia:** Como cliente, quiero recibir por email el comprobante con el código QR, para poder ingresar a la sala y tener el detalle de lo que pagué.

**Criterios de aceptación**

- [ ] Al confirmar la compra se genera **un único QR para toda la compra**, que cubre todas sus entradas (S16).
- [ ] El QR codifica un token aleatorio, único y seguro, generado en Python; nunca un número correlativo (S17).
- [ ] Se envía un email con el comprobante: función, butacas, servicios, precios, total y el QR de la compra (S2).
- [ ] El email incluye un botón "Cancelar compra" que lleva a la página de confirmación de cancelación (S15).
- [ ] La página de confirmación de compra muestra el mismo detalle.
- [ ] Si el envío del email falla, la compra no se pierde y el QR sigue disponible en el perfil.

**Prioridad:** Alta · **Estimación:** 8 SP · **Depende de:** PB-21 · **Endpoints:** `POST /compras`, `GET /compras/{id}`, `GET /compras/{id}/qr`

#### PB-23 · Cancelación de una compra

**Historia:** Como cliente, quiero cancelar una compra hasta 2 horas antes de la función, para liberar las butacas si no puedo asistir.

**Criterios de aceptación**

- [ ] El botón del email abre una página que pide iniciar sesión y muestra el detalle de la compra; **abrir el enlace no cancela nada** (S15).
- [ ] La cancelación ocurre solo cuando el cliente la confirma, y solo el dueño de la compra puede hacerlo (`403`).
- [ ] Se cancela la compra completa: todas sus entradas y servicios; las butacas quedan libres y el QR de la compra deja de ser válido (S14).
- [ ] Si faltan menos de 2 horas para la función, se rechaza (`422`, S13).
- [ ] Una compra ya cancelada o utilizada no se puede cancelar (`409`).
- [ ] La compra cancelada aparece con ese estado en el perfil del cliente.

**Prioridad:** Alta · **Estimación:** 5 SP · **Depende de:** PB-22 · **Endpoints:** `GET /compras/{id}`, `POST /compras/{id}/cancelacion`

### 3.7 Perfil del cliente

#### PB-24 · Historial de compras y consumos

**Historia:** Como cliente, quiero ver en mi perfil todas mis compras y consumos, para tener a mano mis entradas y lo que gasté.

**Criterios de aceptación**

- [ ] Se listan todas las compras del cliente con fecha, película, local, sala, función, butacas, servicios, total y estado (S22).
- [ ] Desde cada compra vigente se puede ver el QR y acceder a la cancelación.
- [ ] Un cliente solo ve sus propias compras.

**Prioridad:** Alta · **Estimación:** 5 SP · **Depende de:** PB-21 · **Endpoints:** `GET /usuarios/me/historial`, `GET /compras/{id}/qr`

#### PB-26 · Películas vistas

**Historia:** Como cliente, quiero ver en mi perfil las películas que vi, para recordar lo que ya fui a ver al cine.

**Criterios de aceptación**

- [ ] Una película figura como vista cuando se validó al menos un QR de una compra del cliente para esa película (S22).
- [ ] Cada película vista muestra póster, título y fecha de la función.
- [ ] Las compras canceladas o sin QR validado no generan películas vistas.

**Prioridad:** Alta · **Estimación:** 2 SP · **Depende de:** PB-24, PB-25 · **Endpoint:** `GET /usuarios/me/historial`

### 3.8 Validación de QR

#### PB-25 · Validación del QR en el ingreso a la sala

**Historia:** Como administrador, quiero escanear o ingresar el código QR en el ingreso a la sala, para permitir la entrada solo con entradas válidas.

**Criterios de aceptación**

- [ ] Solo los administradores acceden a la pantalla "Control de ingreso" (S18).
- [ ] Se puede ingresar el token a mano o escanear el QR, según el mecanismo que acepte el tutor (T1).
- [ ] Se verifica, en este orden, que el token exista, que no esté cancelado ni utilizado, que corresponda a la función que se controla y que se esté dentro de la ventana de 60 minutos antes a 30 minutos después del inicio (S19).
- [ ] Si es válido, la **compra completa** queda como `utilizada`, con la fecha y hora de validación y el administrador que validó; todas sus entradas ingresan juntas (S16).
- [ ] Un QR ya utilizado no puede volver a usarse, aunque se escanee dos veces al mismo tiempo (S17).
- [ ] Si no es válido, se muestra el motivo: inexistente, cancelado, ya utilizado, otra función o fuera de horario.
- [ ] La pantalla muestra los datos de la compra validada (cliente, película, sala, función y todas las butacas).

**Prioridad:** Alta · **Estimación:** 8 SP · **Depende de:** PB-22 · **Endpoint:** `POST /qr/validaciones` · **Mockup:** M-19 · **Nota:** el mecanismo de escaneo depende de T1 (ver D2).

### 3.9 Dashboards

> Todos los dashboards son exclusivos del administrador, admiten filtros por rango de fechas y local, y no cuentan las entradas de compras canceladas como vendidas. La forma de mostrar los gráficos (Chart.js o barras con CSS) depende de la respuesta a T2.

#### PB-27 · Ocupación por función y por película

**Historia:** Como administrador, quiero ver la ocupación por función y por película, para saber qué funciones y películas convocan más público.

**Criterios de aceptación**

- [ ] Se puede agrupar por función o por película.
- [ ] Cada fila muestra la capacidad, las entradas vendidas y el porcentaje de ocupación.
- [ ] Los valores coinciden con un cálculo manual sobre datos de prueba.

**Prioridad:** Alta · **Estimación:** 5 SP · **Depende de:** PB-21 · **Endpoint:** `GET /estadisticas/ocupacion`

#### PB-28 · Ventas por género

**Historia:** Como administrador, quiero ver las entradas vendidas y la recaudación por género, para decidir qué tipo de películas programar.

**Criterios de aceptación**

- [ ] Se muestran, por género, la cantidad de entradas y la recaudación.
- [ ] Una película con varios géneros suma en cada uno de ellos.
- [ ] Se representa como gráfico de barras o tabla, como en el mockup.

**Prioridad:** Alta · **Estimación:** 3 SP · **Depende de:** PB-21 · **Endpoint:** `GET /estadisticas/ventas-por-genero`

#### PB-29 · Franjas horarias más vendidas

**Historia:** Como administrador, quiero ver qué franjas horarias venden más entradas, para ajustar los horarios de las funciones.

**Criterios de aceptación**

- [ ] Las entradas vendidas y la recaudación se agrupan por franja horaria de inicio de la función.
- [ ] Las franjas se ordenan de mayor a menor cantidad de entradas.

**Prioridad:** Alta · **Estimación:** 3 SP · **Depende de:** PB-21 · **Endpoint:** `GET /estadisticas/franjas-horarias` · **Mockup:** M-16

#### PB-30 · Cancelaciones

**Historia:** Como administrador, quiero ver la cantidad y el monto de las cancelaciones, para medir su impacto en las ventas.

**Criterios de aceptación**

- [ ] Se muestran las compras canceladas, las entradas liberadas, el monto y la tasa de cancelación.
- [ ] Se muestra el detalle de cancelaciones por película.

**Prioridad:** Alta · **Estimación:** 3 SP · **Depende de:** PB-23 · **Endpoint:** `GET /estadisticas/cancelaciones`

#### PB-31 · Resumen general con indicadores

**Historia:** Como administrador, quiero ver un resumen general al entrar al Backoffice, para conocer de un vistazo cómo va el negocio.

**Criterios de aceptación**

- [ ] La pantalla "Resumen general" muestra las ventas totales, las entradas vendidas y la ocupación promedio.
- [ ] Incluye los bloques "Ventas por género" y "Ocupación por función".
- [ ] La pantalla "Ventas y estadísticas" muestra las ventas acumuladas, las cancelaciones, los servicios vendidos y las ventas por franja horaria.

**Prioridad:** Media · **Estimación:** 3 SP · **Depende de:** PB-27 a PB-30 · **Endpoint:** `GET /estadisticas/resumen` · **Mockups:** M-10, M-16

### 3.10 Entrega

#### PB-32 · `init.sh` e instrucciones de ejecución

**Historia:** Como corrector, quiero instalar las dependencias y levantar el proyecto siguiendo pasos simples, para evaluarlo sin inconvenientes.

**Criterios de aceptación**

- [ ] Existe un archivo `init.sh` que instala todas las dependencias del backend y del frontend.
- [ ] El `README` explica cómo crear la base, configurar las variables de entorno y ejecutar cada aplicación.
- [ ] Siguiendo esos pasos en un entorno limpio, el sistema queda funcionando.

**Prioridad:** Alta · **Estimación:** 2 SP · **Depende de:** PB-05

#### PB-33 · Informe final del proyecto

**Historia:** Como corrector, quiero un informe del proyecto, para entender las decisiones de diseño antes de corregir.

**Criterios de aceptación**

- [ ] El informe contiene carátula, integrantes, resumen, introducción, solución propuesta, tecnología utilizada y conclusión final.
- [ ] Detalla las principales decisiones de diseño (incluidos los supuestos), las dificultades encontradas y las conclusiones.

**Prioridad:** Alta · **Estimación:** 3 SP · **Depende de:** —

### 3.11 Deseables (fuera del alcance inicial)

> Estas historias solo se abordan si sobra tiempo, según la sección 3 de `alcance-y-supuestos.md`.

#### PB-34 · Reporte PDF de ventas

**Historia:** Como administrador, quiero descargar un PDF con las ventas por función y las películas más vistas, para compartir los resultados.

**Criterios de aceptación**

- [ ] Desde la pantalla "Ventas y estadísticas" se descarga un PDF filtrado por rango de fechas y local.
- [ ] El PDF incluye las ventas por función y el ranking de películas más vistas.

**Prioridad:** Baja · **Estimación:** 5 SP · **Depende de:** PB-27 · **Endpoint:** `GET /reportes/ventas`

#### PB-35 · Reseñas y puntuación de películas

**Historia:** Como cliente que asistió a una función, quiero puntuar y comentar la película, para compartir mi opinión con otros espectadores.

**Criterios de aceptación**

- [ ] Solo pueden publicar reseñas los clientes con un QR validado para esa película (criterio de S22).
- [ ] La reseña tiene una puntuación de 1 a 5 y un comentario.
- [ ] El detalle de la película muestra las reseñas y la puntuación promedio.

**Prioridad:** Baja · **Estimación:** 5 SP · **Depende de:** PB-26 · **Endpoints:** `GET /peliculas/{id}/resenas`, `POST /peliculas/{id}/resenas`

#### PB-36 · Documentación de la API con Swagger

**Historia:** Como integrante del equipo, quiero la documentación de la API en Swagger, para probar los endpoints y consultarlos con ejemplos.

**Criterios de aceptación**

- [ ] Todos los endpoints de `endpoints.md` están documentados con sus parámetros, respuestas y errores.
- [ ] La documentación se puede consultar desde el navegador.

**Prioridad:** Baja · **Estimación:** 3 SP · **Depende de:** PB-04

#### PB-37 · Dockerización del proyecto

**Historia:** Como integrante del equipo, quiero levantar el proyecto con Docker, para tener el mismo entorno en todas las computadoras.

**Criterios de aceptación**

- [ ] Hay imágenes para el backend, el frontend y MySQL.
- [ ] Un solo comando levanta todo el sistema con la base inicializada.

**Prioridad:** Baja · **Estimación:** 3 SP · **Depende de:** PB-32

#### PB-38 · Despliegue en servicios gratuitos

**Historia:** Como cliente de Cine Paradiso, quiero acceder al sistema desde internet, para usarlo sin instalar nada.

**Criterios de aceptación**

- [ ] La aplicación está desplegada en un servicio gratuito (Render, PythonAnywhere, Railway, Koyeb u otro).
- [ ] La base de datos MySQL está alojada en un servicio gratuito.
- [ ] La URL pública está documentada en el `README`.

**Prioridad:** Baja · **Estimación:** 5 SP · **Depende de:** PB-37

---

## 4. Trazabilidad con los requisitos obligatorios

| # | Requisito obligatorio (sección 1.7 de `alcance-y-supuestos.md`) | Historias | Mockup |
|---|---|---|---|
| 1 | Registro, inicio de sesión y roles | PB-06, PB-07, PB-08, PB-09 | M-1, M-18 |
| 2 | Cartelera y detalle de cada película con sus funciones | PB-17, PB-19 | M-2, M-3 |
| 3 | Mapa de butacas libres y ocupadas | PB-13, PB-20 | M-4, M-9 |
| 4 | Compra de entradas y servicios, con checkout | PB-18, PB-21 | M-4, M-17 |
| 5 | Mail con comprobante, QR y enlace de cancelación | PB-22 | M-5, M-6 |
| 6 | Cancelación con límite de tiempo | PB-23 | M-8 |
| 7 | Perfil con historial y películas vistas | PB-24, PB-26 | M-7 |
| 8 | Backoffice: películas, funciones y ABM de servicios | PB-11, PB-12, PB-14, PB-15, PB-18 | M-11 a M-15, M-17 |
| 9 | Validación del QR al ingresar | PB-25 | M-19 |
| 10 | Dashboards: ocupación, ventas por género, franjas horarias y cancelaciones | PB-27, PB-28, PB-29, PB-30 | M-10, M-16 |
| 11 | Seguridad en todos los endpoints | PB-08 | — |
| 12 | Acceso mobile (responsive) | PB-05 | M-9 |
| 13 | Proceso: GitHub con ramas, Kanban, `init.sh`, script SQL e informe | PB-01, PB-02, PB-03, PB-32, PB-33 | — |

Todos los requisitos obligatorios quedan cubiertos por al menos una historia de prioridad Alta.

---


