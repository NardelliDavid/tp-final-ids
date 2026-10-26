-- =====================================================================
-- Cine Paradiso: esquema de base de datos (Hito 1)
-- Motor: MySQL 8.0.16 o superior (necesario para que se apliquen los CHECK).
-- Coherente con el enunciado, con los supuestos S1-S25
-- (alcance-y-supuestos.md) y con el listado de endpoints (endpoints.md),
-- ambos en esta misma carpeta.
--
-- El backend usa SQL explícito (sin ORM). Este script:
--   * NO borra ninguna base existente (no hay DROP DATABASE ni DROP TABLE).
--     Si las tablas ya existen, CREATE TABLE falla y no pisa nada.
--   * Crea las tablas y precarga locales, salas, butacas, géneros y el admin.
--
-- Zona horaria (S24): los DATETIME se guardan en hora de Argentina. El
-- backend debe ejecutar SET time_zone = '-03:00' al abrir cada conexión.
-- Moneda (S24): todos los importes son en ARS.
-- =====================================================================

CREATE DATABASE IF NOT EXISTS cine_paradiso
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

USE cine_paradiso;


-- ---------------------------------------------------------------------
-- USUARIOS (S20, S21)
-- ---------------------------------------------------------------------
-- Se agrega "activo" porque PATCH /usuarios/{id} permite dar de baja.
-- La baja es lógica para no romper el historial de compras.
CREATE TABLE usuarios (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(80)  NOT NULL,
    email         VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol           ENUM('administrador','cliente') NOT NULL DEFAULT 'cliente',
    activo        TINYINT(1)   NOT NULL DEFAULT 1,
    creado_en     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ---------------------------------------------------------------------
-- LOCALES (nueva)
-- ---------------------------------------------------------------------
-- Antes el local era un texto dentro de "salas". Se pasa a tabla propia
-- porque GET /locales devuelve cada local con sus salas, y así el nombre
-- del local no se repite en cada sala.
-- Locales, salas y butacas son fijos (S6): se precargan con este script y
-- no tienen ABM, por eso no llevan columna "activo".
CREATE TABLE locales (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    nombre    VARCHAR(100) NOT NULL UNIQUE,
    direccion VARCHAR(200)
);


-- ---------------------------------------------------------------------
-- SALAS (modificada)
-- ---------------------------------------------------------------------
-- Ahora apunta a "locales" en vez de guardar el local como texto.
-- filas y columnas definen la grilla rectangular de la sala (S7). Como las
-- salas son fijas y todas las butacas son iguales, la capacidad sigue
-- siendo filas * columnas (columna generada del script original).
-- Máximo 26 filas porque se identifican con letras de la A a la Z.
CREATE TABLE salas (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    local_id INT         NOT NULL,
    nombre   VARCHAR(50) NOT NULL,
    filas    TINYINT     NOT NULL,
    columnas TINYINT     NOT NULL,
    capacidad SMALLINT GENERATED ALWAYS AS (filas * columnas) STORED,
    UNIQUE KEY uq_sala_local (local_id, nombre),
    CONSTRAINT chk_sala_filas    CHECK (filas BETWEEN 1 AND 26),
    CONSTRAINT chk_sala_columnas CHECK (columnas BETWEEN 1 AND 50),
    CONSTRAINT fk_sala_local FOREIGN KEY (local_id) REFERENCES locales(id)
);


-- ---------------------------------------------------------------------
-- BUTACAS (nueva)
-- ---------------------------------------------------------------------
-- El enunciado define la butaca como un asiento identificado dentro de una
-- sala. Tenerlas como filas permite que una entrada apunte a una butaca
-- concreta y que la base impida venderla dos veces en la misma función.
-- Identificación S7: fila con letra y número de columna (ej.: C7). La API
-- recibe el código "C7" y el backend lo busca por (sala_id, fila, numero).
CREATE TABLE butacas (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    sala_id INT        NOT NULL,
    fila    CHAR(1)    NOT NULL,
    numero  TINYINT    NOT NULL,
    UNIQUE KEY uq_butaca_sala (sala_id, fila, numero),
    CONSTRAINT chk_butaca_fila   CHECK (fila BETWEEN 'A' AND 'Z'),
    CONSTRAINT chk_butaca_numero CHECK (numero >= 1),
    CONSTRAINT fk_butaca_sala FOREIGN KEY (sala_id) REFERENCES salas(id)
);


-- ---------------------------------------------------------------------
-- GÉNEROS y PELICULA_GENERO (se conservan)
-- ---------------------------------------------------------------------
-- Necesarios para el dashboard de ventas por género.
-- tmdb_id es el identificador del género en TMDB. Al importar una película
-- (POST /peliculas), TMDB devuelve los géneros con su id; el backend los
-- busca por tmdb_id y no por nombre, porque el nombre puede variar según
-- el idioma ("Suspense" / "Suspenso").
CREATE TABLE generos (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    tmdb_id INT         NOT NULL UNIQUE,
    nombre  VARCHAR(50) NOT NULL UNIQUE
);


-- ---------------------------------------------------------------------
-- PELÍCULAS (modificada)
-- ---------------------------------------------------------------------
-- S8/S9: se importan de TMDB (en español) y se guardan acá; la cartelera
-- lee de esta tabla. La clasificación la elige el admin a mano.
-- S10: el período de cartelera pasa a esta tabla (cartelera_desde/hasta).
-- Son DATE porque representan días completos, no un momento puntual; los
-- momentos con fecha y hora usan un único DATETIME (funciones.inicio).
-- "activo" permite la baja lógica (DELETE /peliculas/{id}).
CREATE TABLE peliculas (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    tmdb_id         INT UNIQUE,
    titulo          VARCHAR(200) NOT NULL,
    sinopsis        TEXT,
    poster_url      VARCHAR(500),
    duracion_min    SMALLINT NOT NULL,
    clasificacion   ENUM('ATP','+13','+16','+18') NOT NULL,
    cartelera_desde DATE NOT NULL,
    cartelera_hasta DATE NOT NULL,
    activo          TINYINT(1) NOT NULL DEFAULT 1,
    CONSTRAINT chk_pelicula_duracion CHECK (duracion_min > 0),
    CONSTRAINT chk_pelicula_periodo  CHECK (cartelera_hasta >= cartelera_desde)
);

CREATE TABLE pelicula_genero (
    pelicula_id INT NOT NULL,
    genero_id   INT NOT NULL,
    PRIMARY KEY (pelicula_id, genero_id),
    CONSTRAINT fk_pg_pelicula FOREIGN KEY (pelicula_id) REFERENCES peliculas(id) ON DELETE CASCADE,
    CONSTRAINT fk_pg_genero   FOREIGN KEY (genero_id)   REFERENCES generos(id)
);


-- ---------------------------------------------------------------------
-- FUNCIONES (modificada)
-- ---------------------------------------------------------------------
-- Se elimina la tabla intermedia "cartelera": la función apunta directo a
-- la película y a la sala (S11: el admin indica película, sala, fecha y
-- hora en un único DATETIME, y precio). El precio es por función (S4).
--
-- Reglas S12 que no se pueden expresar con CHECK porque cruzan tablas;
-- las valida el backend dentro de una transacción antes del INSERT/UPDATE:
--   0. Bloquear la sala, para que dos altas simultáneas en la misma sala
--      se ejecuten de a una y no se superpongan entre sí:
--        SELECT id FROM salas WHERE id = %s FOR UPDATE;
--   1. DATE(inicio) entre peliculas.cartelera_desde y cartelera_hasta.
--   2. Sin superposición en la misma sala, dejando 20 min de limpieza.
--      Consulta de ejemplo (nueva función: sala %s, inicio %s, duración %s):
--        SELECT f.id
--        FROM funciones f
--        JOIN peliculas p ON p.id = f.pelicula_id
--        WHERE f.sala_id = %s AND f.activo = 1
--          AND f.inicio < DATE_ADD(%s, INTERVAL %s + 20 MINUTE)
--          AND %s < DATE_ADD(f.inicio, INTERVAL p.duracion_min + 20 MINUTE)
--        FOR UPDATE;
--      Si devuelve filas, la función se pisa con otra.
--   Después se hace el INSERT/UPDATE y el COMMIT (ROLLBACK si algo falla).
--
-- uq_funcion_sala_inicio es una protección mínima a nivel base: impide dos
-- funciones ACTIVAS en la misma sala y a la misma hora. Usa la columna
-- generada sala_activa, que vale NULL cuando la función está dada de baja
-- (activo = 0); como MySQL permite varios NULL en una clave única, una
-- función dada de baja no bloquea que se cree otra en ese horario (baja
-- lógica). Es el mismo mecanismo que entradas.funcion_ocupada.
CREATE TABLE funciones (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    pelicula_id INT           NOT NULL,
    sala_id     INT           NOT NULL,
    inicio      DATETIME      NOT NULL,
    precio      DECIMAL(10,2) NOT NULL,
    activo      TINYINT(1)    NOT NULL DEFAULT 1,
    sala_activa INT GENERATED ALWAYS AS (IF(activo = 1, sala_id, NULL)) STORED,
    UNIQUE KEY uq_funcion_sala_inicio (sala_activa, inicio),
    KEY idx_funcion_sala_inicio (sala_id, inicio),
    KEY idx_funcion_pelicula_inicio (pelicula_id, inicio),
    CONSTRAINT chk_funcion_precio CHECK (precio > 0),
    CONSTRAINT fk_funcion_pelicula FOREIGN KEY (pelicula_id) REFERENCES peliculas(id),
    CONSTRAINT fk_funcion_sala     FOREIGN KEY (sala_id)     REFERENCES salas(id)
);


-- ---------------------------------------------------------------------
-- SERVICIOS (se conserva)
-- ---------------------------------------------------------------------
-- Comida, bebidas, estacionamiento, VIP, etc. Disponibles para todas las
-- salas y sin control de stock (S5). Baja lógica con "activo".
CREATE TABLE servicios (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100)  NOT NULL,
    descripcion VARCHAR(255),
    precio      DECIMAL(10,2) NOT NULL,
    activo      TINYINT(1)    NOT NULL DEFAULT 1,
    CONSTRAINT chk_servicio_precio CHECK (precio >= 0)
);


-- ---------------------------------------------------------------------
-- COMPRAS (modificada)
-- ---------------------------------------------------------------------
-- Una compra es de UNA función (checkout: butacas de una función +
-- servicios). El pago es simulado (S1): al confirmar queda pagada.
--
-- Un único QR por compra (S16, decisión definitiva del grupo): qr_token es
-- un token aleatorio generado en Python (S17), por ejemplo con
-- secrets.token_urlsafe(32) (43 caracteres), y es lo que se codifica en el
-- QR. Un mismo QR habilita el ingreso de todas las entradas de la compra.
--
-- Estados:
--   confirmada -> recién comprada, QR válido.
--   utilizada  -> el admin validó el QR al ingresar (S18, S19). Una sola vez.
--   cancelada  -> el cliente canceló toda la compra hasta 2 h antes (S13-S15).
-- La validación se hace con un UPDATE condicional, que evita usar el QR
-- dos veces aunque lleguen dos escaneos a la vez:
--   UPDATE compras SET estado = 'utilizada', validada_en = NOW(), validada_por = %s
--   WHERE qr_token = %s AND funcion_id = %s AND estado = 'confirmada';
-- (POST /qr/validaciones; antes el backend chequea la ventana de -60/+30 min).
--
-- Checkout (POST /compras), en una única transacción:
--   INSERT INTO compras ...; INSERT INTO entradas ... (una por butaca);
--   INSERT INTO compra_servicios ...; COMMIT.
-- Si una butaca ya está vendida, el INSERT de entradas falla con el error
-- 1062 y se hace ROLLBACK de todo: nunca queda una compra a medias.
-- Cancelación (POST /compras/{id}/cancelacion), en una única transacción:
--   SELECT ... FROM compras WHERE id = %s FOR UPDATE;   (bloquea la compra)
--   UPDATE compras SET estado = 'cancelada', cancelada_en = NOW() WHERE id = %s;
--   UPDATE entradas SET activa = 0 WHERE compra_id = %s;
--   COMMIT.
-- La base no puede impedir por sí sola que una compra cancelada quede con
-- entradas activas; por eso ambos UPDATE van siempre en la misma transacción.
--
-- total se guarda porque es lo que figura en el comprobante enviado por mail.
-- uq_compra_funcion existe solo para que "entradas" pueda referenciar
-- (compra_id, funcion_id) y así asegurar que la entrada es de la misma
-- función que su compra.
CREATE TABLE compras (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id   INT           NOT NULL,
    funcion_id   INT           NOT NULL,
    fecha        DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total        DECIMAL(12,2) NOT NULL,
    estado       ENUM('confirmada','utilizada','cancelada') NOT NULL DEFAULT 'confirmada',
    qr_token     VARCHAR(64)   NOT NULL UNIQUE,
    validada_en  DATETIME,
    validada_por INT,
    cancelada_en DATETIME,
    UNIQUE KEY uq_compra_funcion (id, funcion_id),
    KEY idx_compra_usuario (usuario_id, fecha),
    CONSTRAINT chk_compra_total CHECK (total >= 0),
    -- Las fechas de validación y cancelación tienen que coincidir con el estado.
    CONSTRAINT chk_compra_validada  CHECK ((estado = 'utilizada') = (validada_en IS NOT NULL)),
    CONSTRAINT chk_compra_cancelada CHECK ((estado = 'cancelada') = (cancelada_en IS NOT NULL)),
    CONSTRAINT fk_compra_usuario      FOREIGN KEY (usuario_id)   REFERENCES usuarios(id),
    CONSTRAINT fk_compra_funcion      FOREIGN KEY (funcion_id)   REFERENCES funciones(id),
    CONSTRAINT fk_compra_validada_por FOREIGN KEY (validada_por) REFERENCES usuarios(id)
);


-- ---------------------------------------------------------------------
-- ENTRADAS (modificada)
-- ---------------------------------------------------------------------
-- Una fila por butaca comprada. Ya no tiene QR ni estado propio: ambos
-- son de la compra (S14, S16). Máximo 6 por compra (S3): lo controla el
-- backend antes de insertar.
--
-- Venta duplicada (S23): la clave única uq_funcion_butaca impide que la
-- misma butaca tenga dos entradas activas en la misma función, incluso si
-- dos compras se confirman al mismo tiempo (la segunda falla con error
-- 1062 y el backend hace ROLLBACK). Si la compra se cancela, en la misma
-- transacción se hace
--   UPDATE entradas SET activa = 0 WHERE compra_id = %s;
-- y funcion_ocupada pasa a NULL, lo que libera la butaca (MySQL permite
-- varios NULL en una clave única) sin borrar el historial.
--
-- Butacas ocupadas de una función:
--   SELECT butaca_id FROM entradas WHERE funcion_ocupada = %s;
--
-- El backend también verifica que la butaca pertenezca a la sala de la
-- función (butacas.sala_id = funciones.sala_id). La base NO lo controla:
-- aceptaría una butaca de otra sala, así que esa validación es obligatoria.
CREATE TABLE entradas (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    compra_id       INT           NOT NULL,
    funcion_id      INT           NOT NULL,
    butaca_id       INT           NOT NULL,
    precio          DECIMAL(10,2) NOT NULL,
    activa          TINYINT(1)    NOT NULL DEFAULT 1,
    funcion_ocupada INT GENERATED ALWAYS AS (IF(activa = 1, funcion_id, NULL)) STORED,
    UNIQUE KEY uq_funcion_butaca (funcion_ocupada, butaca_id),
    UNIQUE KEY uq_compra_butaca (compra_id, butaca_id),
    CONSTRAINT chk_entrada_precio CHECK (precio >= 0),
    CONSTRAINT fk_entrada_compra  FOREIGN KEY (compra_id, funcion_id) REFERENCES compras(id, funcion_id),
    CONSTRAINT fk_entrada_funcion FOREIGN KEY (funcion_id) REFERENCES funciones(id),
    CONSTRAINT fk_entrada_butaca  FOREIGN KEY (butaca_id)  REFERENCES butacas(id)
);


-- ---------------------------------------------------------------------
-- COMPRA_SERVICIOS (modificada)
-- ---------------------------------------------------------------------
-- Servicios agregados a una compra. precio_unitario guarda el precio al
-- momento de la compra, por si después el admin lo cambia.
-- Clave primaria compuesta: un servicio aparece una sola vez por compra y
-- se usa "cantidad" (antes se podía repetir la misma fila).
CREATE TABLE compra_servicios (
    compra_id       INT           NOT NULL,
    servicio_id     INT           NOT NULL,
    cantidad        SMALLINT      NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (compra_id, servicio_id),
    CONSTRAINT chk_cs_cantidad CHECK (cantidad > 0),
    CONSTRAINT chk_cs_precio   CHECK (precio_unitario >= 0),
    CONSTRAINT fk_cs_compra   FOREIGN KEY (compra_id)   REFERENCES compras(id),
    CONSTRAINT fk_cs_servicio FOREIGN KEY (servicio_id) REFERENCES servicios(id)
);


-- =====================================================================
-- DATOS INICIALES
-- =====================================================================

-- Administrador (S21). Hash generado con werkzeug (scrypt), tomado del
-- script original.
INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES
('Administrador', 'admin@cineparadiso.com',
 'scrypt:32768:8:1$O5LVFkHA4utaEh3N$547bdbbaf9174db804128272be3eda2d47d735a2e4a3ebd965ea8dca293665ea56feb1e08f206bd9a9e233eeb8a14340a3bcc4f7e111748532e0b5ea7306cd3d',
 'administrador');

-- Los 3 locales y sus salas quedan precargados (S6). Nombres y tamaños
-- tomados del script original. Las direcciones quedan vacías hasta que el
-- grupo las defina.
INSERT INTO locales (id, nombre) VALUES
(1, 'Cine Paradiso Centro'),
(2, 'Cine Paradiso Norte'),
(3, 'Cine Paradiso Sur');

INSERT INTO salas (local_id, nombre, filas, columnas) VALUES
(1, 'Sala 1', 10, 12),
(1, 'Sala 2',  8, 10),
(2, 'Sala 1', 12, 15),
(2, 'Sala 2',  6,  8),
(3, 'Sala 1',  9, 10),
(3, 'Sala 2',  5,  6);

-- Butacas: una por cada fila (A, B, C...) y columna de cada sala.
-- La CTE genera los números del 1 al 50 para no escribir cada butaca a mano.
INSERT INTO butacas (sala_id, fila, numero)
WITH RECURSIVE numeros (n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM numeros WHERE n < 50
)
SELECT s.id, CHAR(64 + f.n USING utf8mb4), c.n
FROM salas s
JOIN numeros f ON f.n <= s.filas
JOIN numeros c ON c.n <= s.columnas
ORDER BY s.id, f.n, c.n;

-- Géneros: la lista completa de géneros de películas de TMDB, con su id y
-- su nombre en español (S9).
INSERT INTO generos (tmdb_id, nombre) VALUES
(28, 'Acción'), (12, 'Aventura'), (16, 'Animación'), (35, 'Comedia'),
(80, 'Crimen'), (99, 'Documental'), (18, 'Drama'), (10751, 'Familia'),
(14, 'Fantasía'), (36, 'Historia'), (27, 'Terror'), (10402, 'Música'),
(9648, 'Misterio'), (10749, 'Romance'), (878, 'Ciencia ficción'),
(10770, 'Película de TV'), (53, 'Suspenso'), (10752, 'Bélica'),
(37, 'Western');
