DROP DATABASE IF EXISTS cine_paradiso;
CREATE DATABASE cine_paradiso;
USE cine_paradiso;

CREATE TABLE usuarios (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(80)  NOT NULL,
    email         VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol           ENUM('administrador','cliente') NOT NULL DEFAULT 'cliente'
);

CREATE TABLE salas (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    local     VARCHAR(100) NOT NULL,
    nombre    VARCHAR(50)  NOT NULL,
    UNIQUE KEY uq_sala_local (local, nombre)
);

CREATE TABLE generos (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE peliculas (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    tmdb_id       INT UNIQUE,
    titulo        VARCHAR(200) NOT NULL,
    sinopsis      TEXT,
    poster_url    VARCHAR(500),
    duracion_min  SMALLINT NOT NULL,
    clasificacion ENUM('ATP','+13','+16','+18') NOT NULL
);

CREATE TABLE pelicula_genero (
    pelicula_id INT NOT NULL,
    genero_id   INT NOT NULL,
    PRIMARY KEY (pelicula_id, genero_id),
    FOREIGN KEY (pelicula_id) REFERENCES peliculas(id) ON DELETE CASCADE,
    FOREIGN KEY (genero_id)   REFERENCES generos(id)
);

CREATE TABLE funciones (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    pelicula_id  INT NOT NULL,
    sala_id      INT NOT NULL,
    inicio       DATETIME NOT NULL,
    fin          DATETIME NOT NULL,
    precio       DECIMAL(10,2) NOT NULL,
    CHECK (fin > inicio),
    FOREIGN KEY (pelicula_id) REFERENCES peliculas(id),
    FOREIGN KEY (sala_id)     REFERENCES salas(id)
);

CREATE TABLE servicios (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    precio      DECIMAL(10,2) NOT NULL,
    activo      TINYINT(1) NOT NULL DEFAULT 1 
);

CREATE TABLE compras (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total      DECIMAL(12,2) NOT NULL,
    codigo_qr  CHAR(100) NOT NULL UNIQUE,
    estado     ENUM('activa','utilizada','cancelada') NOT NULL DEFAULT 'activa',
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE entradas (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    compra_id  INT NOT NULL,
    funcion_id INT NOT NULL,
    fila       SMALLINT NOT NULL,
    columna    SMALLINT NOT NULL,
    precio     DECIMAL(10,2) NOT NULL,
    estado     ENUM('activa','utilizada','cancelada') NOT NULL DEFAULT 'activa',
    FOREIGN KEY (compra_id)  REFERENCES compras(id),
    FOREIGN KEY (funcion_id) REFERENCES funciones(id)
);

CREATE TABLE compra_servicios (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    compra_id       INT NOT NULL,
    servicio_id     INT NOT NULL,
    cantidad        SMALLINT NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (compra_id)   REFERENCES compras(id),
    FOREIGN KEY (servicio_id) REFERENCES servicios(id)
);


-- Datos al inicializar la db
INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES
('Administrador', 'admin@cineparadiso.com',
 'scrypt:32768:8:1$O5LVFkHA4utaEh3N$547bdbbaf9174db804128272be3eda2d47d735a2e4a3ebd965ea8dca293665ea56feb1e08f206bd9a9e233eeb8a14340a3bcc4f7e111748532e0b5ea7306cd3d',
 'administrador');

INSERT INTO salas (local, nombre) VALUES
('Cine Paradiso Centro', 'Sala 1'),
('Cine Paradiso Centro', 'Sala 2'),
('Cine Paradiso Norte',  'Sala 1'),
('Cine Paradiso Norte',  'Sala 2'),
('Cine Paradiso Sur',    'Sala 1'),
('Cine Paradiso Sur',    'Sala 2');

INSERT INTO generos (nombre) VALUES
('Acción'), ('Aventura'), ('Animación'), ('Comedia'), ('Crimen'),
('Documental'), ('Drama'), ('Familia'), ('Fantasía'), ('Historia'),
('Terror'), ('Música'), ('Misterio'), ('Romance'), ('Ciencia ficción'),
('Suspenso'), ('Bélica'), ('Western');


INSERT INTO peliculas (tmdb_id, titulo, sinopsis, poster_url, duracion_min, clasificacion) VALUES
(238,   'El Padrino', 'La saga de la familia Corleone, una de las más poderosas del crimen organizado de Nueva York, y el ascenso de su hijo menor al mando.', NULL, 175, '+16'),
(680,   'Tiempos violentos', 'Historias cruzadas de dos sicarios, un boxeador y la esposa de un mafioso en Los Ángeles.', NULL, 154, '+18'),
(105,   'Volver al futuro', 'Un adolescente viaja accidentalmente al pasado en una máquina del tiempo y debe asegurarse de que sus padres se enamoren.', NULL, 116, 'ATP'),
(289,   'Casablanca', 'En plena Segunda Guerra Mundial, un dueño de bar en Marruecos se reencuentra con un amor del pasado.', NULL, 102, 'ATP'),
(11216, 'Cinema Paradiso', 'Un director recuerda su infancia en un pequeño pueblo de Sicilia y su amistad con el proyeccionista del cine local.', NULL, 124, '+13'),
(78,    'Blade Runner', 'En un Los Ángeles futurista, un cazador de androides persigue a un grupo de replicantes fugitivos.', NULL, 117, '+16');

INSERT INTO pelicula_genero (pelicula_id, genero_id)
SELECT p.id, g.id
FROM peliculas p
JOIN generos g ON
    (p.titulo = 'El Padrino'         AND g.nombre IN ('Drama', 'Crimen'))
 OR (p.titulo = 'Tiempos violentos'  AND g.nombre IN ('Crimen', 'Suspenso'))
 OR (p.titulo = 'Volver al futuro'   AND g.nombre IN ('Aventura', 'Comedia', 'Ciencia ficción'))
 OR (p.titulo = 'Casablanca'         AND g.nombre IN ('Drama', 'Romance'))
 OR (p.titulo = 'Cinema Paradiso'    AND g.nombre IN ('Drama', 'Romance'))
 OR (p.titulo = 'Blade Runner'       AND g.nombre IN ('Ciencia ficción', 'Suspenso'));
