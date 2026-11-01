from db.conexion_db import *

def consultar_peliculas_disponibles_db():
    conn = None
    cursor = None

    try:
        conn = conexion()
        cursor = conn.cursor()

        consulta_sql = "SELECT * FROM peliculas;"
        cursor.execute(consulta_sql)

        consulta = cursor.fetchall()

        respuesta = {"OK": consulta}, 200

    except Exception as e:
        respuesta = {"Error": str(e)}, 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return respuesta

def agregar_pelicula_db(pelicula):
    conn = None
    cursor = None

    try:
        conn = conexion()
        cursor = conn.cursor()

        consulta_sql = """
            INSERT INTO peliculas
            (tmdb_id, titulo, sinopsis, poster_url, duracion_min, clasificacion)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = (
            pelicula["tmdb_id"],
            pelicula["titulo"],
            pelicula["sinopsis"],
            pelicula["poster"],
            pelicula["duracion"],
            "+18"
        )

        cursor.execute(consulta_sql, valores)

        # Obtiene el id de la pelicula insertada 
        id_pelicula = cursor.lastrowid

        # Inserta los generos de la pelicula y sus relaciones
        for nombre_genero in pelicula["generos"]:
            cursor.execute(
                "SELECT id FROM generos WHERE nombre = %s",
                (nombre_genero,)
            )
            resultado = cursor.fetchone()

            if resultado is None:
                respuesta = {"Error": f"El género {nombre_genero} no existe en la BD"}, 400
            else:
                id_genero = resultado[0]

                cursor.execute(
                    """INSERT INTO pelicula_genero (pelicula_id, genero_id)
                       VALUES (%s, %s)""",
                    (id_pelicula, id_genero)
                )

                respuesta = {"OK": "Película y géneros insertados correctamente"}, 200

        conn.commit()

    except Exception as e:
        if conn:
            conn.rollback()

        respuesta = {"Error": str(e)}, 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return respuesta

def eliminar_pelicula_db(id_pelicula):
    conn = None
    cursor = None

    try:
        conn = conexion()
        cursor = conn.cursor()

        consulta_sql = """
            DELETE FROM peliculas WHERE tmdb_id = %s
        """

        cursor.execute(consulta_sql, (id_pelicula,))
        conn.commit()

        respuesta = {"OK": "Película eliminada correctamente"}, 200

    except Exception as e:
        if conn:
            conn.rollback()

        respuesta = {"Error": str(e)}, 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return respuesta