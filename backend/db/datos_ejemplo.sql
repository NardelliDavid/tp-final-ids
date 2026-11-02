
USE cine_paradiso;

INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES
('Administrador', 'admin@cineparadiso.com',
 'scrypt:32768:8:1$O5LVFkHA4utaEh3N$547bdbbaf9174db804128272be3eda2d47d735a2e4a3ebd965ea8dca293665ea56feb1e08f206bd9a9e233eeb8a14340a3bcc4f7e111748532e0b5ea7306cd3d',
 'administrador');

INSERT INTO salas (local, nombre, filas, columnas) VALUES
('Cine Paradiso Centro', 'Sala 1', 10, 12),
('Cine Paradiso Centro', 'Sala 2', 8, 10),
('Cine Paradiso Norte',  'Sala 1', 12, 15),
('Cine Paradiso Norte',  'Sala 2', 6, 8),
('Cine Paradiso Sur',    'Sala 1', 9, 12),
('Cine Paradiso Sur',    'Sala 2', 7, 10);

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


-- CLIENTES (el admin ya es id 1)
INSERT INTO usuarios (id, nombre, email, password_hash, rol) VALUES
(2, 'Lucía Fernández', 'lucia@mail.com',  'hash_demo_2', 'cliente'),
(3, 'Martín Gómez',    'martin@mail.com', 'hash_demo_3', 'cliente'),
(4, 'Sofía Ramírez',   'sofia@mail.com',  'hash_demo_4', 'cliente');

-- SERVICIOS
INSERT INTO servicios (id, nombre, descripcion, precio, activo) VALUES
(1, 'Pochoclo grande', 'Balde de pochoclo salado o dulce', 3500.00, 1),
(2, 'Gaseosa',         'Vaso de 500 ml',                    2500.00, 1),
(3, 'Combo pareja',    '2 gaseosas + pochoclo grande',      7500.00, 1),
(4, 'Nachos',          'Nachos con cheddar',                3000.00, 1);

-- FUNCIONES (sala 1, 2 y 3 existen en tu script)
INSERT INTO funciones (id, pelicula_id, sala_id, inicio, fin, precio) VALUES
(1, (SELECT id FROM peliculas WHERE titulo = 'Blade Runner'),      1, NOW() - INTERVAL 4 DAY,  NOW() - INTERVAL 4 DAY  + INTERVAL 3 HOUR, 5000.00),
(2, (SELECT id FROM peliculas WHERE titulo = 'Tiempos violentos'), 2, NOW() - INTERVAL 9 DAY,  NOW() - INTERVAL 9 DAY  + INTERVAL 3 HOUR, 4500.00),
(3, (SELECT id FROM peliculas WHERE titulo = 'Volver al futuro'),  3, NOW() - INTERVAL 2 DAY,  NOW() - INTERVAL 2 DAY  + INTERVAL 2 HOUR, 4000.00),
(4, (SELECT id FROM peliculas WHERE titulo = 'El Padrino'),        1, NOW() - INTERVAL 14 DAY, NOW() - INTERVAL 14 DAY + INTERVAL 3 HOUR, 5000.00),
(5, (SELECT id FROM peliculas WHERE titulo = 'Cinema Paradiso'),   2, NOW() - INTERVAL 44 DAY, NOW() - INTERVAL 44 DAY + INTERVAL 2 HOUR, 4500.00);

-- COMPRAS
INSERT INTO compras (id, usuario_id, fecha, total, codigo_qr, estado) VALUES
(1, 2, NOW() - INTERVAL 5  DAY, 18500.00, 'QR-DEMO-0001', 'activa'),
(2, 3, NOW() - INTERVAL 10 DAY, 21000.00, 'QR-DEMO-0002', 'utilizada'),
(3, 4, NOW() - INTERVAL 3  DAY, 17500.00, 'QR-DEMO-0003', 'activa'),
(4, 2, NOW() - INTERVAL 15 DAY, 17000.00, 'QR-DEMO-0004', 'activa'),
(5, 3, NOW() - INTERVAL 8  DAY, 17500.00, 'QR-DEMO-0005', 'cancelada'),  -- compra cancelada
(6, 4, NOW() - INTERVAL 20 DAY, 13500.00, 'QR-DEMO-0006', 'activa'),     -- tiene 1 entrada cancelada
(7, 2, NOW() - INTERVAL 45 DAY, 12500.00, 'QR-DEMO-0007', 'utilizada'),  -- fuera del último mes
(8, 3, NOW() - INTERVAL 2  DAY, 17000.00, 'QR-DEMO-0008', 'activa');

-- ENTRADAS
INSERT INTO entradas (id, compra_id, funcion_id, fila, columna, precio, estado) VALUES
(1,  1, 1, 3, 5, 5000.00, 'activa'),
(2,  1, 1, 3, 6, 5000.00, 'activa'),
(3,  2, 2, 4, 2, 4500.00, 'utilizada'),
(4,  2, 2, 4, 3, 4500.00, 'utilizada'),
(5,  2, 2, 4, 4, 4500.00, 'utilizada'),
(6,  3, 3, 5, 7, 4000.00, 'activa'),
(7,  3, 3, 5, 8, 4000.00, 'activa'),
(8,  3, 3, 5, 6, 4000.00, 'activa'),
(9,  4, 4, 2, 5, 5000.00, 'activa'),
(10, 4, 4, 2, 6, 5000.00, 'activa'),
(11, 5, 1, 6, 1, 5000.00, 'cancelada'),
(12, 5, 1, 6, 2, 5000.00, 'cancelada'),
(13, 6, 1, 7, 3, 5000.00, 'activa'),
(14, 6, 1, 7, 4, 5000.00, 'activa'),
(15, 6, 1, 7, 5, 5000.00, 'cancelada'),
(16, 7, 5, 1, 1, 4500.00, 'utilizada'),
(17, 7, 5, 1, 2, 4500.00, 'utilizada'),
(18, 8, 2, 5, 5, 4500.00, 'activa'),
(19, 8, 1, 8, 8, 5000.00, 'activa');

-- SERVICIOS COMPRADOS
INSERT INTO compra_servicios (compra_id, servicio_id, cantidad, precio_unitario) VALUES
(1, 1, 1, 3500.00),
(1, 2, 2, 2500.00),
(2, 3, 1, 7500.00),
(3, 2, 1, 2500.00),
(3, 4, 1, 3000.00),
(4, 1, 2, 3500.00),
(5, 3, 1, 7500.00),   -- compra cancelada
(6, 1, 1, 3500.00),
(7, 1, 1, 3500.00),   -- fuera del último mes
(8, 3, 1, 7500.00);