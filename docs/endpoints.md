# Cine Paradiso: listado de endpoints


##  Resumen de endpoints

| # | Módulo | Método | Ruta | Rol |
|---|---|---|---|---|
| 1 | Autenticación | `POST` | `/auth/registro` | Público |
| 2 | Autenticación | `POST` | `/auth/login` | Público |
| 3 | Películas | `GET` | `/tmdb/peliculas` | Admin |
| 4 | Películas | `POST` | `/peliculas` | Admin |
| 5 | Películas | `GET` | `/peliculas` | Admin |
| 6 | Películas | `GET` | `/peliculas/{id}` | Público |
| 7 | Películas | `PATCH` | `/peliculas/{id}` | Admin |
| 8 | Películas | `DELETE` | `/peliculas/{id}` | Admin |
| 9 | Cartelera | `GET` | `/cartelera` | Público |
| 10 | Cartelera | `GET` | `/locales` | Público |
| 11 | Funciones | `GET` | `/funciones` | Público |
| 12 | Funciones | `GET` | `/funciones/{id}` | Público |
| 13 | Funciones | `GET` | `/funciones/{id}/butacas` | Público |
| 14 | Funciones | `POST` | `/funciones` | Admin |
| 15 | Funciones | `PATCH` | `/funciones/{id}` | Admin |
| 16 | Funciones | `DELETE` | `/funciones/{id}` | Admin |
| 17 | Compras | `POST` | `/compras` | Cliente |
| 18 | Compras | `GET` | `/compras/{id}` | Dueño |
| 19 | Compras | `POST` | `/compras/{id}/cancelacion` | Dueño |
| 20 | Servicios | `GET` | `/servicios` | Público |
| 21 | Servicios | `POST` | `/servicios` | Admin |
| 22 | Servicios | `PATCH` | `/servicios/{id}` | Admin |
| 23 | Servicios | `DELETE` | `/servicios/{id}` | Admin |
| 24 | Perfil | `GET` | `/usuarios/me` | Autenticado |
| 25 | Perfil | `PATCH` | `/usuarios/me` | Autenticado |
| 26 | Perfil | `GET` | `/usuarios/me/historial` | Cliente |
| 27 | Administración | `GET` | `/usuarios` | Admin |
| 28 | Administración | `GET` | `/usuarios/{id}` | Admin |
| 29 | Administración | `PATCH` | `/usuarios/{id}` | Admin |
| 30 | Administración | `GET` | `/estadisticas/resumen` | Admin |
| 31 | Administración | `GET` | `/estadisticas/ocupacion` | Admin |
| 32 | Administración | `GET` | `/estadisticas/ventas-por-genero` | Admin |
| 33 | Administración | `GET` | `/estadisticas/franjas-horarias` | Admin |
| 34 | Administración | `GET` | `/estadisticas/cancelaciones` | Admin |
| 35 | QR | `GET` | `/compras/{id}/qr` | Dueño |
| 36 | QR | `POST` | `/qr/validaciones` | Admin |



---

## 3. Autenticación

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| `POST` | `/auth/registro` | Registra un cliente nuevo. | Público |
| `POST` | `/auth/login` | Inicia sesión y devuelve un token. | Público |

### `POST /auth/registro`

Registra un cliente. El backend asigna siempre el rol cliente y guarda la contraseña con un hash seguro (S20). La cuenta del administrador no se crea por aquí, sino en la inicialización del sistema (S21).

**Entrada**

```json
{ "nombre": "Ana Pérez", "email": "ana@mail.com", "password": "********" }
```

**Salida `201`**

```json
{ "id": 15, "nombre": "Ana Pérez", "email": "ana@mail.com", "rol": "cliente" }
```

**Errores:** `409` correo ya registrado · `400` faltan campos o el formato del correo es inválido.

### `POST /auth/login`

Verifica las credenciales y devuelve un token para los pedidos siguientes.

**Entrada**

```json
{ "email": "ana@mail.com", "password": "********" }
```

**Salida `200`**

```json
{
  "token": "eyJhbGciOi...",
  "usuario": { "id": 15, "nombre": "Ana Pérez", "email": "ana@mail.com", "rol": "cliente" }
}
```

**Errores:** `401` credenciales incorrectas · `403` usuario dado de baja.

El cierre de sesión no necesita un endpoint: el frontend borra el token de la sesión de Flask.

---

## 4. Películas

Las películas se importan desde **TMDB** y se guardan en MySQL. La cartelera consulta siempre nuestra base de datos, no la API externa (S8). Los datos se piden a TMDB en español y la clasificación por edades la elige el administrador (S9).

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| `GET` | `/tmdb/peliculas` | Busca películas en TMDB para importarlas. | Admin |
| `POST` | `/peliculas` | Importa una película de TMDB y define su período de cartelera. | Admin |
| `GET` | `/peliculas` | Lista el catálogo completo importado. | Admin |
| `GET` | `/peliculas/{id}` | Detalle de una película. | Público |
| `PATCH` | `/peliculas/{id}` | Modifica sinopsis, póster, clasificación o período de cartelera. | Admin |
| `DELETE` | `/peliculas/{id}` | Da de baja una película (baja lógica). | Admin |

### `GET /tmdb/peliculas`

El backend consulta la búsqueda de TMDB (en español) y devuelve los resultados. Marca las que ya están importadas para evitar duplicados.

**Parámetros:** `q` (texto a buscar, obligatorio) · `pagina` (opcional, por defecto 1).

**Salida `200`**

```json
[
  {
    "tmdb_id": 11216,
    "titulo": "Cinema Paradiso",
    "anio": 1988,
    "sinopsis": "Salvatore, un director de cine...",
    "poster_url": "https://image.tmdb.org/t/p/w500/...jpg",
    "ya_importada": false
  }
]
```

**Errores:** `400` falta `q` · `502` TMDB no respondió.

### `POST /peliculas`

Importa una película. El backend obtiene de TMDB el título, la sinopsis, el póster, la duración y los géneros, y guarda todo en MySQL junto con los datos que carga el administrador. Los géneros se asocian por su identificador de TMDB (columna `generos.tmdb_id`), no por el nombre. El período de cartelera indica el tiempo en que la película estará disponible (S10).

**Entrada**

```json
{
  "tmdb_id": 11216,
  "clasificacion": "ATP",
  "cartelera_desde": "2026-11-01",
  "cartelera_hasta": "2026-11-30"
}
```

`clasificacion` usa la escala argentina (por ejemplo, `ATP`, `+13`, `+16`, `+18`).

**Salida `201`:** la película creada, con el mismo formato que `GET /peliculas/{id}`.

**Errores:** `409` la película ya fue importada · `422` `cartelera_hasta` es anterior a `cartelera_desde` · `404` el `tmdb_id` no existe en TMDB · `502` TMDB no respondió.

### `GET /peliculas`

Lista todas las películas importadas, incluidas las que no están en cartelera. Sirve para la gestión desde el backoffice.

**Parámetros (opcionales):** `q` (título) · `genero` · `clasificacion` · `activo` (`true`/`false`) · `vigente` (`true`/`false`).

**Salida `200`:** lista de películas con `id`, `titulo`, `poster_url`, `generos`, `clasificacion`, `cartelera_desde`, `cartelera_hasta` y `activo`. El frontend muestra "En cartelera" si hoy está dentro del período y "Próximamente" si `cartelera_desde` es posterior a hoy.

### `GET /peliculas/{id}`

Detalle de una película para la cartelera: sinopsis, póster, duración y clasificación (enunciado). Las funciones disponibles se consultan con `GET /funciones?pelicula_id={id}`.

**Salida `200`**

```json
{
  "id": 7,
  "tmdb_id": 11216,
  "titulo": "Cinema Paradiso",
  "sinopsis": "Salvatore, un director de cine...",
  "poster_url": "https://image.tmdb.org/t/p/w500/...jpg",
  "duracion_min": 155,
  "clasificacion": "ATP",
  "generos": ["Drama", "Romance"],
  "cartelera_desde": "2026-11-01",
  "cartelera_hasta": "2026-11-30"
}
```

**Errores:** `404` no existe o está dada de baja.

### `PATCH /peliculas/{id}`

Modifica los datos editables por el administrador: sinopsis y póster (S8), clasificación (S9) y período de cartelera (S10). Los demás datos provienen de TMDB y no se editan.

**Entrada (todos los campos son opcionales)**

```json
{
  "sinopsis": "Texto corregido...",
  "poster_url": "https://...",
  "clasificacion": "+13",
  "cartelera_desde": "2026-11-01",
  "cartelera_hasta": "2026-12-15"
}
```

**Salida `200`:** la película actualizada.

**Errores:** `404` no existe · `422` el nuevo período deja funciones ya programadas fuera de él (S10).

### `DELETE /peliculas/{id}`

Da de baja la película (baja lógica): deja de aparecer en la cartelera y no se pueden programar nuevas funciones. Las compras y estadísticas anteriores se conservan.

**Salida:** `204`.

**Errores:** `404` no existe · `409` tiene funciones futuras activas.

---

## 5. Cartelera

La cartelera es el conjunto de películas y funciones vigentes. Los locales y las salas están precargados en la base de datos y son fijos: no se crean, modifican ni eliminan desde el sistema (S6). Por eso solo tienen endpoints de consulta.

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| `GET` | `/cartelera` | Películas en cartel, con filtros. | Público |
| `GET` | `/locales` | Los 3 locales con sus salas y capacidades. | Público |

### `GET /cartelera`

Devuelve las películas activas cuyo período de cartelera incluye la fecha consultada y que tienen al menos una función futura.

**Parámetros (opcionales):** `fecha` (por defecto, hoy) · `local_id` · `genero`.

**Salida `200`**

```json
[
  {
    "id": 7,
    "titulo": "Cinema Paradiso",
    "poster_url": "https://image.tmdb.org/t/p/w500/...jpg",
    "duracion_min": 155,
    "clasificacion": "ATP",
    "generos": ["Drama", "Romance"],
    "cartelera_hasta": "2026-11-30"
  }
]
```

### `GET /locales`

Lista los locales con sus salas. Cubre el acceso a la capacidad de cada sala; la disponibilidad por función se consulta en `GET /funciones/{id}/butacas`.

**Salida `200`**

```json
[
  {
    "id": 1,
    "nombre": "Cine Paradiso Centro",
    "salas": [
      { "id": 1, "nombre": "Sala 1", "filas": 10, "columnas": 12, "capacidad": 120 },
      { "id": 2, "nombre": "Sala 2", "filas": 8, "columnas": 10, "capacidad": 80 }
    ]
  }
]
```

---

## 6. Funciones

Una función es una película proyectada en una sala, en una fecha y hora puntuales. El administrador crea cada función manualmente (S11) y el precio se define por función (S4).

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| `GET` | `/funciones` | Lista funciones, con filtros. | Público |
| `GET` | `/funciones/{id}` | Detalle de una función. | Público |
| `GET` | `/funciones/{id}/butacas` | Mapa de butacas libres y ocupadas. | Público |
| `POST` | `/funciones` | Crea una función. | Admin |
| `PATCH` | `/funciones/{id}` | Modifica una función. | Admin |
| `DELETE` | `/funciones/{id}` | Da de baja una función (baja lógica). | Admin |

### `GET /funciones`

Para el público devuelve solo funciones futuras y activas. El administrador puede ver también las pasadas o dadas de baja con `incluir_pasadas=true`.

**Parámetros (opcionales):** `pelicula_id` · `local_id` · `sala_id` · `fecha` (un día) · `desde` y `hasta` (rango de días, para la vista semanal de programación) · `incluir_pasadas` (solo Admin).

**Salida `200`**

```json
[
  {
    "id": 31,
    "pelicula": { "id": 7, "titulo": "Cinema Paradiso" },
    "local": { "id": 1, "nombre": "Cine Paradiso Centro" },
    "sala": { "id": 2, "nombre": "Sala 2" },
    "inicio": "2026-11-05T20:30:00",
    "precio": 4500.00,
    "butacas_libres": 64
  }
]
```

### `GET /funciones/{id}`

Detalle de una función, con los mismos campos que el listado más la capacidad de la sala.

**Errores:** `404` no existe.

### `GET /funciones/{id}/butacas`

Devuelve la grilla de la sala con el estado de cada butaca para esa función. Una butaca está ocupada si pertenece a una compra que no fue cancelada.

**Salida `200`**

```json
{
  "funcion_id": 31,
  "filas": 8,
  "columnas": 10,
  "butacas": [
    { "codigo": "A1", "fila": "A", "numero": 1, "estado": "libre" },
    { "codigo": "A2", "fila": "A", "numero": 2, "estado": "ocupada" }
  ]
}
```

**Errores:** `404` la función no existe.

### `POST /funciones`

Crea una función. El backend valida las reglas de S12:

- La fecha tiene que estar dentro del período de cartelera de la película (S10).
- No puede superponerse con otra función de la misma sala.
- Tiene que dejar 20 minutos de limpieza entre el fin de una proyección (inicio + duración) y el inicio de la siguiente.

**Entrada**

```json
{ "pelicula_id": 7, "sala_id": 2, "inicio": "2026-11-05T20:30:00", "precio": 4500.00 }
```

**Salida `201`:** la función creada.

**Errores:** `404` la película o la sala no existen · `422` fuera del período de cartelera, en el pasado o superpuesta (incluido el margen de limpieza).

### `PATCH /funciones/{id}`

Modifica `sala_id`, `inicio` o `precio`. Se vuelven a validar las reglas de S12.

**Salida `200`:** la función actualizada.

**Errores:** `404` no existe · `409` la función ya tiene compras activas · `422` no cumple las reglas de S12.

### `DELETE /funciones/{id}`

Da de baja la función (baja lógica).

**Salida:** `204`.

**Errores:** `404` no existe · `409` la función ya tiene compras activas.

---

## 7. Compras

Una compra corresponde a **una sola función**, incluye de 1 a 6 entradas (S3) y, opcionalmente, servicios adicionales (S5). Tiene un **único código QR** para todas sus entradas (S16). El pago es **simulado**: al confirmar el checkout la compra queda pagada, sin pasarela de pago (S1). Por eso no hay un endpoint de pago aparte.

Estados de una compra: `confirmada` (pagada) → `utilizada` (cuando se valida el QR) o `cancelada`.

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| `POST` | `/compras` | Checkout: entradas y servicios, pago simulado, QR y correo. | Cliente |
| `GET` | `/compras/{id}` | Detalle de una compra. | Dueño |
| `POST` | `/compras/{id}/cancelacion` | Cancela la compra completa. | Dueño |

### `POST /compras`

Realiza el checkout en una sola operación:

1. Valida la función, las butacas y los servicios.
2. Registra la compra con el pago simulado (S1). MySQL impide que una butaca se venda dos veces, incluso con compras simultáneas (S23). No hay reservas temporales.
3. Genera el token aleatorio del QR de la compra (S17).
4. Envía por correo el comprobante (entradas, servicios, precios y total), el QR y el botón para cancelar (S2).

**Validaciones y transacción en el backend.** Algunas reglas cruzan tablas y la base no las puede garantizar sola, así que las controla el backend antes de insertar:

- La función existe, está activa y todavía no empezó.
- Hay entre 1 y 6 butacas, sin repetir (S3).
- Cada butaca existe **y pertenece a la sala de la función**. La base aceptaría una butaca de otra sala, así que este control es obligatorio.
- Cada servicio existe y está activo. El precio de cada entrada se toma de la función y el de cada servicio, del servicio (no del pedido).

Los pasos 2 y 3 se hacen en **una única transacción**: `INSERT` en `compras`, `INSERT` de cada entrada y de cada servicio, y `COMMIT`. Si una butaca ya está vendida, MySQL rechaza el `INSERT` con el error 1062 (clave `uq_funcion_butaca`); el backend hace `ROLLBACK` completo y responde `409`. Así nunca queda una compra con solo una parte de sus entradas. El correo se envía después del `COMMIT`: si falla, la compra se conserva y el QR sigue disponible en el perfil.

**Entrada**

```json
{
  "funcion_id": 31,
  "butacas": ["C7", "C8"],
  "servicios": [
    { "servicio_id": 3, "cantidad": 2 }
  ]
}
```

**Salida `201`**

```json
{
  "id": 120,
  "estado": "confirmada",
  "fecha": "2026-11-02T18:12:45",
  "funcion": {
    "id": 31,
    "pelicula": "Cinema Paradiso",
    "local": "Cine Paradiso Centro",
    "sala": "Sala 2",
    "inicio": "2026-11-05T20:30:00"
  },
  "entradas": [
    { "butaca": "C7", "precio": 4500.00 },
    { "butaca": "C8", "precio": 4500.00 }
  ],
  "servicios": [
    { "servicio_id": 3, "nombre": "Combo pochoclos", "cantidad": 2, "precio_unitario": 3000.00, "subtotal": 6000.00 }
  ],
  "total": 15000.00
}
```

**Errores:** `409` alguna butaca ya está ocupada (`BUTACA_OCUPADA`) · `422` más de 6 entradas o ninguna (`CANTIDAD_ENTRADAS`), butaca inexistente en la sala, función pasada o dada de baja, servicio inactivo · `404` la función no existe.

### `GET /compras/{id}`

Detalle de una compra, con el mismo formato que la respuesta de `POST /compras`. También lo usa la página de confirmación de la cancelación (S15).

**Errores:** `403` si no es el cliente  · `404` no existe.

### `POST /compras/{id}/cancelacion`

Cancela la **compra completa**: todas sus entradas y servicios. Libera las butacas e invalida el QR (S14). Solo se permite hasta 2 horas antes del inicio de la función (S13).

El botón del correo abre una página del frontend que muestra la compra y pide confirmar. Abrir el enlace no cancela nada: la cancelación ocurre recién cuando el cliente confirma y el frontend llama a este endpoint (S15). Como el pago es simulado, no hay reintegro real (S1).

**Transacción en el backend.** La cancelación cambia la compra y sus entradas a la vez, para que nunca queden desalineadas (por ejemplo, una compra cancelada con butacas todavía ocupadas). En una única transacción:

1. `SELECT ... FOR UPDATE` de la compra, para bloquearla mientras se valida.
2. Se verifica que el usuario sea el dueño, que el estado sea `confirmada` y que falten al menos 2 horas para la función.
3. `UPDATE compras SET estado = 'cancelada', cancelada_en = NOW()`.
4. `UPDATE entradas SET activa = 0 WHERE compra_id = ...` (libera las butacas).
5. `COMMIT`. Ante cualquier error, `ROLLBACK`.

El bloqueo del paso 1 evita que una cancelación y una validación del QR de la misma compra se pisen.

**Entrada:** sin cuerpo.

**Salida `200`**

```json
{ "id": 120, "estado": "cancelada", "cancelada_en": "2026-11-04T10:05:00" }
```

**Errores:** `403` si no es el cliente · `404` no existe · `409` la compra ya está cancelada o utilizada · `422` faltan menos de 2 horas para la función (`FUERA_DE_PLAZO`).

---

## 8. Servicios

Servicios adicionales (comida, bebidas, estacionamiento, acceso VIP, entre otros) disponibles para todas las salas (enunciado). No tienen control de stock y se compran junto con las entradas (S5).

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| `GET` | `/servicios` | Lista los servicios. | Público |
| `POST` | `/servicios` | Crea un servicio. | Admin |
| `PATCH` | `/servicios/{id}` | Modifica un servicio. | Admin |
| `DELETE` | `/servicios/{id}` | Da de baja un servicio (baja lógica). | Admin |

### `GET /servicios`

Para el público devuelve solo los servicios activos. El administrador puede incluir los inactivos con `incluir_inactivos=true`.

**Salida `200`**

```json
[
  { "id": 3, "nombre": "Combo pochoclos", "descripcion": "Pochoclos grandes y gaseosa", "precio": 3000.00, "activo": true }
]
```

### `POST /servicios`

**Entrada**

```json
{ "nombre": "Estacionamiento", "descripcion": "Por 3 horas", "precio": 2000.00 }
```

**Salida `201`:** el servicio creado.

**Errores:** `400` faltan campos · `422` precio negativo.

### `PATCH /servicios/{id}`

Modifica `nombre`, `descripcion` o `precio`. También permite reactivar un servicio dado de baja con `"activo": true`. Las compras anteriores conservan el precio que tenían al momento de comprar.

**Salida `200`:** el servicio actualizado.

**Errores:** `404` no existe · `422` precio negativo.

### `DELETE /servicios/{id}`

Da de baja el servicio: deja de ofrecerse en nuevas compras.

**Salida:** `204`.

**Errores:** `404` no existe.

---

## 9. Perfil

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| `GET` | `/usuarios/me` | Datos del usuario con sesión iniciada. | Autenticado |
| `PATCH` | `/usuarios/me` | Modifica el nombre o la contraseña propios. | Autenticado |
| `GET` | `/usuarios/me/historial` | Compras, consumos y películas vistas. | Cliente |

### `GET /usuarios/me`

**Salida `200`**

```json
{ "id": 15, "nombre": "Ana Pérez", "email": "ana@mail.com", "rol": "cliente" }
```

### `PATCH /usuarios/me`

**Entrada (campos opcionales)**

```json
{ "nombre": "Ana María Pérez", "password_actual": "********", "password_nueva": "********" }
```

Para cambiar la contraseña hay que enviar la actual.

**Salida `200`:** el usuario actualizado.

**Errores:** `401` la contraseña actual es incorrecta · `400` datos inválidos.

### `GET /usuarios/me/historial`

Reúne en una sola respuesta lo que el perfil muestra en una misma sección (S22): el historial de compras con su estado, los consumos (servicios) y las películas vistas. Una película figura como vista cuando el QR de una compra del cliente para esa película fue validado.

**Salida `200`**

```json
{
  "compras": [
    {
      "id": 120,
      "fecha": "2026-11-02T18:12:45",
      "estado": "utilizada",
      "pelicula": "Cinema Paradiso",
      "local": "Cine Paradiso Centro",
      "sala": "Sala 2",
      "inicio": "2026-11-05T20:30:00",
      "butacas": ["C7", "C8"],
      "servicios": [ { "nombre": "Combo pochoclos", "cantidad": 2 } ],
      "total": 15000.00
    }
  ],
  "peliculas_vistas": [
    { "pelicula_id": 7, "titulo": "Cinema Paradiso", "poster_url": "https://...", "fecha_funcion": "2026-11-05T20:30:00" }
  ]
}
```

---

## 10. Administración

### 10.1 Usuarios

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| `GET` | `/usuarios` | Lista los usuarios. | Admin |
| `GET` | `/usuarios/{id}` | Detalle de un usuario. | Admin |
| `PATCH` | `/usuarios/{id}` | Cambia el rol o da de baja a un usuario. | Admin |

#### `GET /usuarios`

**Parámetros (opcionales):** `q` (nombre o correo) · `rol` · `activo`.

**Salida `200`:** lista con `id`, `nombre`, `email`, `rol` y `activo`.

#### `GET /usuarios/{id}`

**Salida `200`:** datos del usuario y cantidad de compras.

**Errores:** `404` no existe.

#### `PATCH /usuarios/{id}`

**Entrada (campos opcionales)**

```json
{ "rol": "administrador", "activo": false }
```

Un usuario dado de baja no puede iniciar sesión.

**Salida `200`:** el usuario actualizado.

**Errores:** `404` no existe · `422` rol inválido.

### 10.2 Dashboards

Todos aceptan los filtros opcionales `desde`, `hasta` (fechas de función) y `local_id`. Las entradas de compras canceladas no cuentan como vendidas.

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| `GET` | `/estadisticas/resumen` | Indicadores generales del período. | Admin |
| `GET` | `/estadisticas/ocupacion` | Ocupación por función o por película. | Admin |
| `GET` | `/estadisticas/ventas-por-genero` | Entradas y recaudación por género. | Admin |
| `GET` | `/estadisticas/franjas-horarias` | Franjas horarias más vendidas. | Admin |
| `GET` | `/estadisticas/cancelaciones` | Cantidad y monto de cancelaciones. | Admin |

#### `GET /estadisticas/resumen`

Indicadores que se muestran en las tarjetas de las pantallas "Resumen general" y "Ventas y estadísticas" del Backoffice.

**Salida `200`**

```json
{
  "ventas_totales": 10295000.00,
  "recaudacion_entradas": 5580000.00,
  "recaudacion_servicios": 4715000.00,
  "entradas_vendidas": 1240,
  "servicios_vendidos": 1150,
  "ocupacion_promedio_pct": 64.0,
  "compras_canceladas": 38
}
```

`ventas_totales` es la suma de los totales de las compras no canceladas (entradas más servicios). `servicios_vendidos` es la suma de las cantidades de servicios de esas compras. `ocupacion_promedio_pct` es el total de entradas vendidas sobre la capacidad total de las funciones del período.

#### `GET /estadisticas/ocupacion`

**Parámetro adicional:** `agrupar_por` = `funcion` (por defecto) o `pelicula`.

**Salida `200` (agrupado por película)**

```json
[
  { "pelicula_id": 7, "titulo": "Cinema Paradiso", "funciones": 12, "capacidad_total": 960, "vendidas": 610, "ocupacion_pct": 63.5 }
]
```

Agrupado por función, cada elemento trae `funcion_id`, `pelicula`, `sala`, `inicio`, `capacidad`, `vendidas` y `ocupacion_pct`.

#### `GET /estadisticas/ventas-por-genero`

**Salida `200`**

```json
[
  { "genero": "Drama", "entradas": 1450, "recaudacion": 6525000.00 }
]
```

Una película con varios géneros suma en cada uno de ellos.

#### `GET /estadisticas/franjas-horarias`

Agrupa las entradas vendidas en franjas de una hora según la hora de inicio de la función, ordenadas de mayor a menor.

**Salida `200`**

```json
[
  { "franja": "20:00-21:00", "entradas": 980, "recaudacion": 4410000.00 }
]
```

#### `GET /estadisticas/cancelaciones`

**Salida `200`**

```json
{
  "compras_canceladas": 42,
  "entradas_liberadas": 97,
  "monto": 436500.00,
  "tasa_cancelacion_pct": 4.1,
  "por_pelicula": [ { "pelicula_id": 7, "titulo": "Cinema Paradiso", "compras_canceladas": 9 } ]
}
```

---

## 11. QR

Cada compra tiene un **único QR** para todas sus entradas (S16). Al validarlo, la compra completa queda como `utilizada`. El QR codifica un token aleatorio, único y seguro, generado en Python (S17), y solo puede validarse una vez. Únicamente los administradores lo validan, desde el backoffice (S18).

| Método | Ruta | Descripción | Rol |
|---|---|---|---|
| `GET` | `/compras/{id}/qr` | Devuelve el QR de la compra. | Cliente |
| `POST` | `/qr/validaciones` | Valida el QR en el ingreso a la sala y lo marca como utilizado. | Admin |

### `GET /compras/{id}/qr`

Devuelve el QR para mostrarlo en el perfil del cliente. Es el mismo QR que se envía por correo.

**Salida `200`**

```json
{
  "compra_id": 120,
  "estado": "confirmada",
  "token": "Xq3v9Lr2k8ZpT0mWc5bN1yHf7sJd4aEu6gQiOtRlVxA",
  "imagen_png_base64": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

**Errores:** `403` si no es el cliente · `404` no existe · `409` la compra está cancelada.

### `POST /qr/validaciones`

El administrador elige en el backoffice la función que está controlando y envía el token leído del QR. El backend verifica, en este orden:

1. Que el token exista.
2. Que la compra no esté cancelada (S14) ni haya sido utilizada (S17).
3. Que la compra corresponda a esa función.
4. Que el momento de la validación esté dentro de la ventana permitida: desde 60 minutos antes hasta 30 minutos después del inicio de la función (S19).

Si todo es correcto, marca la compra como `utilizada` y registra la fecha y hora de validación y el administrador que validó. Ese cambio se hace con un único `UPDATE` condicional (`... WHERE qr_token = %s AND funcion_id = %s AND estado = 'confirmada'`, ver `Tablas.sql`): si dos escaneos llegan a la vez, solo uno modifica la fila y el otro recibe `QR_UTILIZADO`. Las entradas no cambian, porque una compra utilizada sigue ocupando sus butacas.

**Entrada**

```json
{ "token": "Xq3v9Lr2k8ZpT0mWc5bN1yHf7sJd4aEu6gQiOtRlVxA", "funcion_id": 31 }
```

**Salida `200`**

```json
{
  "valido": true,
  "compra_id": 120,
  "cliente": "Ana Pérez",
  "pelicula": "Cinema Paradiso",
  "sala": "Sala 2",
  "inicio": "2026-11-05T20:30:00",
  "butacas": ["C7", "C8"],
  "validada_en": "2026-11-05T20:05:12"
}
```

**Errores:** `404` token inexistente (`QR_INEXISTENTE`) · `409` compra cancelada (`QR_CANCELADO`) o ya utilizada (`QR_UTILIZADO`) · `422` corresponde a otra función (`FUNCION_INCORRECTA`) o está fuera de la ventana horaria (`FUERA_DE_VENTANA`).
