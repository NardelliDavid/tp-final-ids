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

        # Verifica si la película ya está agregada
        cursor.execute(
            "SELECT id FROM peliculas WHERE tmdb_id = %s",
            (pelicula["tmdb_id"],)
        )
        existente = cursor.fetchone()

        if existente is not None:
            respuesta = {"Error": "La pelicula ya esta agregada"}, 409
        else:
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

            # Inserta las relaciones con los generos
            genero_invalido = None
            for nombre_genero in pelicula["generos"]:
                cursor.execute(
                    "SELECT id FROM generos WHERE nombre = %s",
                    (nombre_genero,)
                )
                resultado = cursor.fetchone()

                if resultado is None:
                    genero_invalido = nombre_genero
                    break

                cursor.execute(
                    """INSERT INTO pelicula_genero (pelicula_id, genero_id)
                       VALUES (%s, %s)""",
                    (id_pelicula, resultado[0])
                )

            if genero_invalido is not None:
                conn.rollback()
                respuesta = {"Error": f"El genero {genero_invalido} no existe en la BD"}, 400
            else:
                conn.commit()
                respuesta = {"OK": "Pelicula y generos insertados correctamente"}, 200

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

def eliminar_pelicula_db(tmdb_id):
    conn = None
    cursor = None

    try:
        conn = conexion()
        cursor = conn.cursor()

        # Buscar el id interno a partir del id de TMDB
        cursor.execute("SELECT id FROM peliculas WHERE tmdb_id = %s", (tmdb_id,))
        fila = cursor.fetchone()

        if fila is None:
            respuesta = {"Error": "La película no existe"}, 404
        else:
            id_interno = fila[0]

            cursor.execute(
                "SELECT COUNT(*) FROM funciones WHERE pelicula_id = %s",
                (id_interno,)
            )
            cantidad = cursor.fetchone()[0]

            if cantidad > 0:
                respuesta = {
                    "Error": "La pelicula tiene funciones asociadas. Elimina las funciones primero."
                }, 409
            else:
                cursor.execute("DELETE FROM peliculas WHERE id = %s", (id_interno,))
                conn.commit()
                respuesta = {"OK": "Pelicula eliminada correctamente"}, 200

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

def es_admin(email):
    try:
        conn = conexion()
        cursor = conn.cursor()
        respuesta = False

        consulta_sql = """
            SELECT rol FROM usuarios WHERE email = %s AND rol = 'administrador';
        """

        cursor.execute(consulta_sql, (email,))

        if cursor.fetchone():
            respuesta = True

    except Exception as e:
        respuesta = False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return respuesta