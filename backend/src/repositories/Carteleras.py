
from db.conexion_db import conexion


# GET /cartelera
def obtener_cartelera():
    #abre el canal de comunicacion con MySQL
    conn = conexion()
    # abre el canal para ejecutar las consultas MySQL y traer los registros
    cursor = conn.cursor(dictionary=True)

    consulta = """
        SELECT DISTINCT
            peliculas.id,
            peliculas.titulo,
            peliculas.poster_url,
            peliculas.duracion_min,
            peliculas.clasificacion
        FROM peliculas
        INNER JOIN funciones
            ON peliculas.id = funciones.pelicula_id
        WHERE funciones.estado = 'activa'
        ORDER BY peliculas.titulo ASC
    """

    cursor.execute(consulta)
    peliculas = cursor.fetchall()

    # se cierran para liberar memoria y no agotar el límite de conexiones de la base de datos
    cursor.close()
    conn.close()

    return peliculas


def obtener_generos_pelicula(pelicula_id):
    conn = conexion()
    cursor = conn.cursor()

    consulta = """
        SELECT generos.nombre
        FROM generos
        INNER JOIN pelicula_genero
            ON generos.id = pelicula_genero.genero_id
        WHERE pelicula_genero.pelicula_id = %s
    """

    cursor.execute(consulta, (pelicula_id,))
    generos = cursor.fetchall()

    cursor.close()
    conn.close()

    return generos


# GET /locales
def obtener_locales():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    consulta = """
        SELECT
            local,
            id,
            nombre,
            filas,
            columnas
        FROM salas
        ORDER BY local, id
    """

    cursor.execute(consulta)
    salas = cursor.fetchall()

    cursor.close()
    conn.close()

    return salas

# GET /peliculas/<id>/funciones
def obtener_pelicula(pelicula_id):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    consulta = """
        SELECT id, titulo, sinopsis, poster_url, duracion_min, clasificacion
        FROM peliculas
        WHERE id = %s
    """

    cursor.execute(consulta, (pelicula_id,))
    pelicula = cursor.fetchone()

    cursor.close()
    conn.close()

    return pelicula


def obtener_funciones_pelicula(pelicula_id):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    consulta = """
        SELECT
            funciones.id,
            funciones.inicio,
            funciones.fin,
            funciones.precio,
            salas.local,
            salas.nombre AS sala
        FROM funciones
        INNER JOIN salas
            ON funciones.sala_id = salas.id
        WHERE funciones.pelicula_id = %s
        AND funciones.estado = 'activa'
        ORDER BY funciones.inicio ASC
    """

    cursor.execute(consulta, (pelicula_id,))
    funciones = cursor.fetchall()

    cursor.close()
    conn.close()

    return funciones