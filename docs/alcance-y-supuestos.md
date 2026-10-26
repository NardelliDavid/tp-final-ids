# Cine Paradiso: alcance y supuestos

| | |
|---|---|
| **Materia** | Introducción al Desarrollo de Software, FIUBA (Cátedra Lanzillotta, 2.º cuatrimestre 2026) |
| **Entrega** | Hito 1 (26/10/2026) |
| **Fuente** | Enunciado oficial: [`Proyecto integrador IDS 2026.pdf`](Proyecto%20integrador%20IDS%202026.pdf) |
| **Documentos relacionados** | [`endpoints.md`](endpoints.md) · [`product-backlog.md`](product-backlog.md) · [`Tablas.sql`](Tablas.sql) · [`Mockups.pdf`](Mockups.pdf) |

## Índice

1. [Glosario](#glosario)
2. [Requisitos obligatorios](#1-requisitos-obligatorios)
3. [Supuestos](#2-supuestos)
4. [Funcionalidades deseables y fuera de alcance](#3-funcionalidades-deseables-no-obligatorias)


---

## Glosario

| Término | Definición |
|---|---|
| **Supuesto** | Decisión que toma el equipo porque el enunciado no la define. Se deja por escrito para que el corrector sepa cómo la interpretamos. |
| **Alcance** | Límite que separa lo que el sistema **va a hacer** de lo que **no va a hacer**. |
| **Función** | Película proyectada en una sala determinada, en una fecha y horario puntuales. Cada función tiene sus propias butacas disponibles. |
| **Butaca** | Asiento identificado dentro de una sala. No puede venderse dos veces en la misma función. |
| **Cartelera** | Conjunto de películas y funciones vigentes que el cine ofrece al público. |
| **Compra** | Operación de checkout de un cliente para una función: incluye entradas y, opcionalmente, servicios. |
| **Entrada** | Derecho a ocupar una butaca determinada en una función. |
| **Servicio** | Producto adicional que se compra junto con las entradas (comida, bebida, estacionamiento, acceso VIP, etc.). |

---

## 1. Requisitos obligatorios

Todo lo de esta sección está definido explícitamente en el enunciado. No es negociable.

### 1.1 Negocio

- El cine tiene 3 locales, con salas de distinta capacidad de butacas.
- Una butaca no puede venderse dos veces en la misma función.
- La cancelación solo se permite hasta un tiempo determinado antes de la función. El enunciado no fija ese tiempo (ver S13).

### 1.2 Front (usuarios finales)

- Manejo de usuarios con dos roles: administrador y cliente.
- Perfil del cliente con información sobre sus consumos y las películas que vio anteriormente.
- Cartelera con las películas en cartel: sinopsis, póster, duración, clasificación y funciones disponibles.
- Acceso a la capacidad y la disponibilidad de butacas de cada sala.
- Compra de entradas con un flujo ágil: película → función → selección de butacas (mostrando las ocupadas y las libres) → confirmación al email. Se genera un QR con los datos de la compra, que se envía por mail junto con un botón para cancelar.
- Compra de servicios: comida, bebidas, estacionamiento, acceso VIP, entre otros.
- Checkout de la compra con envío de la factura por mail, junto con un QR que permite el ingreso a la sala.

### 1.3 Backoffice (administrador)

- Cargar películas, imágenes y sinopsis, indicando sala, capacidad, local y período en que la película estará disponible.
- Dashboards informativos: ocupación por función y por película, ventas por género, franjas horarias más vendidas y cancelaciones.
- Cargar, modificar y dar de baja servicios. Los servicios están disponibles para todas las salas.
- Validación al ingresar a la sala: al escanear el QR se verifica que corresponda a esa función y fecha y que no haya sido usado ni cancelado. Después se marca como usado.
- El catálogo de películas se obtiene de una API gratuita (OMDb o TMDB).

### 1.4 Técnicos

- **Backend** en Flask: se conecta a la base de datos y expone endpoints que usan el verbo HTTP correcto y el formato JSON.
- **Frontend** en Flask: se conecta al backend respetando RESTful.
- La comunicación entre el frontend y el backend se hace en Python, con la librería `requests`.
- **Prohibido** hacer pedidos desde el navegador (`fetch`, promises, `axios`, `XMLHttpRequest` u otros equivalentes).
- **Prohibido** usar ORMs (SQLAlchemy, SQLModel, Django ORM, Peewee u otros), incluidas las clases de Python que mapeen tablas. Todas las consultas se escriben como sentencias SQL explícitas.
- Base de datos **MySQL**, con al menos 3 tablas y un script de creación y carga.
- La fecha y la hora van en un único campo `DATETIME`, nunca en dos campos separados.
- Todos los endpoints deben tener seguridad.
- Generación de códigos QR y un mecanismo de validación o escaneo.
- Acceso desde dispositivos móviles: web responsive, o una app mobile hecha únicamente con Kivy.
- Si se usan dependencias, un archivo `init.sh` que las instale.

### 1.5 Proceso y entrega

- Repositorio en GitHub compartido con el corrector, con ramas adecuadas al proyecto.
- **Todos** los integrantes hacen commits. Cada commit está asociado a una tarea y su mensaje explica qué se hizo.
- Tablero Kanban con las tareas y el backlog de producto (GitHub Projects, Trello o Jira).
- Cada hito tiene que entregar valor al cliente.
- Informe final con: carátula, integrantes, resumen, introducción, solución propuesta, tecnología utilizada y conclusión final, detallando las principales decisiones de diseño, las dificultades encontradas y las conclusiones.
- Defensa oral grupal e individual.

### 1.6 Condiciones de aprobación

- **No** se pueden usar variables globales ni ciclos infinitos, ni escribir código repetido.
- **No** se puede entregar un programa que no funcione o que tenga errores graves, ni entregar fuera de fecha.
- **Sí** hay que evitar que el programa se rompa cuando el usuario interactúa con él, modularizar el código y aplicar buenas prácticas de programación.

### 1.7 Resumen de funcionalidades obligatorias

| # | Funcionalidad |
|---|---|
| 1 | Registro, inicio de sesión y roles (administrador y cliente). |
| 2 | Cartelera y detalle de cada película con sus funciones. |
| 3 | Mapa de butacas que muestre las libres y las ocupadas. |
| 4 | Compra de entradas y servicios, con checkout. |
| 5 | Mail con el comprobante, el QR y el enlace de cancelación. |
| 6 | Cancelación con límite de tiempo. |
| 7 | Perfil del cliente con su historial y las películas vistas. |
| 8 | Backoffice: películas (desde la API externa), funciones y ABM de servicios. |
| 9 | Validación del QR al ingresar. |
| 10 | Dashboards: ocupación, ventas por género, franjas horarias y cancelaciones. |
| 11 | Seguridad en todos los endpoints. |
| 12 | Acceso mobile (responsive o Kivy). |
| 13 | Requisitos de proceso: GitHub con ramas, Kanban, `init.sh`, script SQL e informe. |

---

## 2. Supuestos

Criterio general: **lo más simple que cumpla el enunciado.**

Los supuestos son **decisiones del equipo**, no requisitos de la cátedra. La única excepción es S1, que confirmó el profesor.

### 2.1 Resumen de supuestos

| Supuesto | Tema |
|---|---|
| S1 | Pago simulado |
| S2 | Comprobante de compra por email |
| S3 | Máximo de 6 entradas por compra |
| S4 | Precio por función |
| S5 | Servicios opcionales sin stock |
| S6 | Locales y salas fijos y precargados |
| S7 | Identificación de butacas |
| S8 | Importación de películas a MySQL |
| S9 | TMDB en español y clasificación manual |
| S10 | Período de cartelera |
| S11 | Creación manual de funciones |
| S12 | Reglas de las funciones |
| S13 | Cancelación hasta 2 horas antes |
| S14 | Cancelación de la compra completa |
| S15 | Cancelación con autenticación y confirmación |
| S16 | Un único QR por compra |
| S17 | Token aleatorio de un solo uso |
| S18 | Solo los administradores validan QR |
| S19 | Ventana de validación del QR |
| S20 | Registro de clientes |
| S21 | Administrador creado en la inicialización |
| S22 | Perfil y películas vistas |
| S23 | Sin reservas temporales de butacas |
| S24 | Moneda, zona horaria e idioma |
| S25 | Web responsive |

### 2.2 Compra y pago

**S1. Pago simulado.** *(Confirmado por el profesor.)*
Los pagos son siempre simulados. No se integran pasarelas de pago reales (Mercado Pago, tarjetas). Al confirmar el checkout, la compra queda como pagada.
*Por qué:* el enunciado no pide pagos, e integrar una pasarela real agrega mucha complejidad y riesgo.

**S2. Comprobante de compra por email.**
Se envía por email un comprobante de compra con las entradas, los servicios, los precios, el total y el código QR de la compra. No se requiere factura fiscal (AFIP/ARCA).

**S3. Máximo de 6 entradas por compra.**
Cada compra incluye entre 1 y 6 entradas.
*Por qué:* es lo habitual en un cine (ir con amigos o en familia), y el límite evita abusos.

**S4. Precio por función.**
El precio se establece por función, y todas las butacas de esa función cuestan lo mismo. La experiencia "VIP" se vende como servicio, que es lo que propone el enunciado.
*Por qué:* permite, por ejemplo, que una función de matiné sea más barata, sin complicar el modelo.

**S5. Servicios opcionales, sin control de stock.**
Los servicios adicionales son opcionales, se compran junto con las entradas y no tienen control de stock.
*Por qué:* así hay un solo flujo de compra.

### 2.3 Locales, salas y películas

**S6. Locales y salas fijos y precargados.**
Los 3 locales y sus salas son fijos: se precargan en MySQL con el script SQL y no se crean, modifican ni eliminan desde el sistema. No hay ABM de locales ni de salas.
*Por qué:* el enunciado dice que el cine "tiene" 3 locales, como un dato fijo. Lo que el administrador configura es qué película se proyecta en cada sala.

**S7. Identificación de las butacas.**
Las filas se identifican con letras y las columnas con números (por ejemplo, C7). Las salas tienen una distribución rectangular y todas las butacas son del mismo tipo.
*Por qué:* permite dibujar la sala como una grilla, algo fácil de hacer en HTML sin JavaScript.

**S8. Importación de películas a MySQL.**
El administrador importa las películas desde una API externa y las guarda en MySQL. Después puede modificar la sinopsis y el póster. La cartelera consulta nuestra base de datos, no la API externa.
*Por qué:* si la API se cae o se agota la cuota gratuita, la cartelera sigue funcionando. Además, es más rápido.

**S9. TMDB en español y clasificación manual.**
Se usa TMDB y se le pide la información en español. El administrador elige a mano la clasificación por edades.
*Por qué:* TMDB devuelve los datos en español. OMDb los devuelve en inglés y con la clasificación de Estados Unidos (PG-13, R), que no corresponde a la Argentina.

**S10. Período de cartelera.**
Cada película tiene un período de cartelera con fecha de inicio y fecha de fin. Las funciones tienen que programarse dentro de ese período.

### 2.4 Funciones

**S11. Creación manual de funciones.**
El administrador crea a mano cada función, indicando la película, la sala, la fecha y hora (en un único campo `DATETIME`) y el precio.

**S12. Reglas de las funciones.**

- Tienen que respetar el período de cartelera de la película.
- No pueden superponerse en la misma sala.
- Tienen que dejar 20 minutos de limpieza entre una proyección y la siguiente.

### 2.5 Cancelaciones

**S13. Cancelación hasta 2 horas antes.**
Una compra se puede cancelar hasta 2 horas antes del inicio de la función.

**S14. Cancelación de la compra completa.**
La cancelación afecta a la compra completa, con todas sus entradas y servicios. Las butacas se liberan y el QR de la compra se invalida. Como el pago es simulado (S1), no hay devolución real de dinero: la compra solo cambia de estado.

**S15. Cancelación con autenticación y confirmación.**
El botón del correo abre una página de Cine Paradiso, donde el cliente tiene que autenticarse y confirmar la cancelación. **Abrir el enlace no cancela la compra automáticamente.**
*Por qué:* si el enlace cancelara directamente, cualquiera que viera el mail (o un antivirus que revisa los enlaces) podría cancelar la compra sin querer.

### 2.6 Códigos QR

**S16. Un único QR por compra.** *(Decisión definitiva del grupo.)*
Cada compra tiene un único código QR, que cubre todas sus entradas. Al validarlo, la compra completa queda como utilizada y todas sus entradas ingresan juntas. Si se cancela la compra, el QR deja de ser válido (S14).

**S17. Token aleatorio de un solo uso.**
Cada compra tiene un token aleatorio, único y seguro, generado en Python, que es lo que se codifica en el QR. El backend verifica que cada QR se pueda usar una sola vez.
*Por qué:* si el QR tuviera un número correlativo (1, 2, 3...), cualquiera podría fabricar QR falsos.

**S18. Solo los administradores validan QR.**
Solamente los administradores pueden escanear y validar códigos QR, desde el Backoffice. No se agrega un rol de "boletero".

**S19. Ventana de validación.**
Los QR se pueden validar desde 60 minutos antes hasta 30 minutos después del inicio de la función.

### 2.7 Usuarios

**S20. Registro de clientes.**
Los clientes se registran con nombre, correo electrónico (único) y contraseña. La contraseña se guarda protegida con un hash seguro. El backend asigna el rol cliente.

**S21. Administrador creado en la inicialización.**
La cuenta del administrador se crea al inicializar el sistema, con la contraseña protegida con un hash seguro. No hay registro público de administradores.

**S22. Perfil y películas vistas.**

- El perfil muestra todas las compras del usuario con sus estados ("consumos").
- Una película aparece como **vista** si se validó el QR de al menos una compra del usuario para esa película.

**Limitación:** este criterio **no prueba que el comprador haya asistido en persona**. El QR habilita el ingreso de toda la compra, así que la película figura como vista para el comprador aunque hayan ingresado solo sus acompañantes.

### 2.8 Concurrencia y configuración

**S23. Sin reservas temporales de butacas.**
No hay reservas temporales: las butacas se asignan al confirmar la compra. MySQL tiene que impedir ventas duplicadas, incluso cuando dos compras se hacen al mismo tiempo.
*Por qué:* las reservas con temporizador ("tenés 10 minutos") son complejas. La base de datos puede garantizar por sí sola que una butaca no se venda dos veces.

**S24. Moneda, zona horaria e idioma.**
Moneda: pesos argentinos (ARS). Zona horaria: Argentina. Idioma: español.

**S25. Web responsive.**
Se desarrolla una web responsive con Flask, HTML, CSS, Jinja2 y Bootstrap, que se adapta a computadoras, tablets y celulares. No se desarrolla una app con Kivy.
*Por qué:* así hay un solo frontend en lugar de dos.

---

## 3. Funcionalidades deseables (no obligatorias)

**No se compromete ninguna en el alcance inicial.** Se listan como posibles mejoras y se suman solo si sobra tiempo, así no queda nada prometido sin cumplir.

| Deseable | Origen | Esfuerzo estimado |
|---|---|---|
| Documentación de endpoints (Swagger o README) | Requisitos generales deseables | Bajo. Además, ayuda mucho al propio equipo. |
| PDF con reporte de ventas por función y películas más vistas | Enunciado de Cine Paradiso | Medio. |
| Reseñas habilitadas solo para usuarios con el QR validado | Enunciado de Cine Paradiso | Medio. Con S22 queda casi resuelto. |
| Dockerizar el proyecto | Enunciado de Cine Paradiso | Medio. |
| Hostear la app y la base de datos en servicios gratuitos | Enunciado y requisitos generales | Medio o alto: el MySQL gratuito es lo más difícil de conseguir. |

### 3.1 Fuera de alcance

Lo siguiente **no** se va a desarrollar. Surge de los supuestos anteriores:

- Pagos reales (S1, confirmado por el profesor).
- Factura fiscal (S2).
- Recuperación de contraseña.
- Verificación de email al registrarse.
- Reserva temporal de butacas (S23).
- Promociones y descuentos.
- Butacas especiales, como accesibles o dobles (S7).
- ABM de locales y salas (S6).

---

## 4. Preguntas para el tutor

### 4.1 Pendientes

| # | Pregunta | Supuesto o requisito relacionado | Respuesta |
|---|---|---|---|
| T1 | ¿Cómo es el proceso de escaneo del QR?
