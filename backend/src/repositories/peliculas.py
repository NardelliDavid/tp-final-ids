from db.conexion_db import *

def consultar_peliculas_disponibles_db():
    return consultar_db("SELECT * FROM peliculas;")

def agregar_pelicla_db(pelicula):
    tmdb_id = pelicula['tmdb_id']
    titulo = pelicula['titulo']
    poster = pelicula['poster']
    duracion = pelicula['duracion']
    sinopsis = pelicula['sinopsis']

    consulta_sql = """
        INSERT INTO peliculas
        (tmdb_id, titulo, sinopsis, poster_url, duracion_min, clasificacion)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (tmdb_id, titulo, sinopsis, poster, duracion, "+18")

    resultado = insertar_datos(consulta_sql, valores)

    return resultado

def eliminar_pelicula_db(id_pelicula):
    consulta_sql = """
        DELETE FROM peliculas WHERE id = %s
    """
    resultado = eliminar_datos(consulta_sql, (id_pelicula,))

    return resultado