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
    nombre    VARCHAR(50) NOT NULL,
    filas     SMALLINT UNSIGNED NOT NULL,
    columnas  SMALLINT UNSIGNED NOT NULL,
    CHECK (filas > 0),
    CHECK (columnas > 0),
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