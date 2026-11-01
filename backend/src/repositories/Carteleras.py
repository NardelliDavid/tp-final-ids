
from backend.db.conexion_db import conexion


# GET /cartelera
def obtener_cartelera(fecha, local, genero):
    conn = conexion()
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
        INNER JOIN salas
            ON funciones.sala_id = salas.id
        WHERE DATE(funciones.inicio) >= %s
        AND funciones.estado = 'activa'
    """

    parametros = [fecha]

    if local is not None:
        consulta += " AND salas.local = %s"
        parametros.append(local)

    if genero is not None:
        consulta += """
            AND EXISTS (
                SELECT 1
                FROM pelicula_genero
                INNER JOIN generos
                    ON pelicula_genero.genero_id = generos.id
                WHERE pelicula_genero.pelicula_id = peliculas.id
                AND generos.nombre = %s
            )
        """
        parametros.append(genero)

    consulta += " ORDER BY peliculas.titulo ASC"

    cursor.execute(consulta, parametros)
    peliculas = cursor.fetchall()

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
