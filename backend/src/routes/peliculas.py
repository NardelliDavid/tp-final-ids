import requests
from flask import jsonify, Blueprint, request
from ..repositories.peliculas import *
from ..validators.peliculas import *

peliculas_bp = Blueprint("peliculas", __name__)

# Endpoint para consultar las peliculas cargadas en la base de datos
@peliculas_bp.route("/backoffice/peliculas", methods=["GET"])
def ver_peliculas_disponibles_db():
    try:
        consulta = consultar_peliculas_disponibles_db()
        resultado = jsonify(consulta), 200
    except Exception as e:
        resultado = jsonify({"Error":str(e)}), 500
    return resultado

# Endpoint para buscar peliculas en TMDB por titulo
@peliculas_bp.route("/backoffice/buscar_peliculas_tmdb", methods=["GET"])
def buscar_peliculas_tmdb():
    try:
        # Obtiene el titulo de la pelicula como parametro, verifica si existe y si es valido
        titulo = request.args.get("titulo")
        if not titulo:
            respuesta = jsonify({"Error": "Falta el parámetro 'titulo' en la URL"}), 400
        else:
            titulo = titulo.strip().lower()
            mensage, codigo = validar_titulo_pelicula(titulo)
            if codigo == 400:
                respuesta = jsonify(mensage), codigo
            elif codigo == 200:
                # Manda la solicitud a la API para obtener las peliculas
                respuesta_api = requests.get(
                    "https://api.themoviedb.org/3/search/movie",
                    params={"api_key": "79e023a83d1ee13b7cf5e31d33cafdea", 
                            "language": "es-AR", 
                            "region": "AR",
                            "query": titulo}, 
                    timeout=5,
                )
                respuesta_api.raise_for_status() # revisa el código de estado HTTP de la respuesta
                datos = respuesta_api.json() # el .json() convierte el JSON recibido de TMDB en un diccionario

                # Filtra los resultados de la api para obtener los datos que nos interesan (id, nombre, sinopsis, año, poster)
                datos["results"].sort(key=lambda p: p["popularity"], reverse=True)
                peliculas = []
                for item in datos["results"]:
                    poster = item.get("poster_path")

                    peliculas.append({
                        "tmdb_id": item["id"],
                        "nombre": item["title"],
                        "sinopsis": item["overview"],
                        "poster": f"https://image.tmdb.org/t/p/w500{poster}" if poster else None,
                    })

                respuesta = jsonify(peliculas), 200 
        
    except Exception as e:
        respuesta = jsonify({"Error":str(e)}), 400
    return respuesta

# Endpoint para agregar la pelicula buscada por id a la base de datos
@peliculas_bp.route("/backoffice/agregar_pelicula_tmdb", methods=["POST"])
def agregar_pelicula_tmdb():
    id_pelicula = request.json.get("id")
    if not id_pelicula:
        respuesta = jsonify({"Error": "No se envio el campo 'id'"}), 400
    else:
        try:
            # Manda la solicitud a la API para obtener la pelicula que se desea agregar
            respuesta_api = requests.get(
                f"https://api.themoviedb.org/3/movie/{id_pelicula}",
                params={"api_key": "79e023a83d1ee13b7cf5e31d33cafdea", 
                        "language": "es-AR", 
                        "region": "AR",
                        }, 
                timeout=5,
            )
            respuesta_api.raise_for_status() # revisa el código de estado HTTP de la respuesta
            datos = respuesta_api.json()

            nombres_generos = []
            for genero in datos["genres"]:
                nombres_generos.append(genero["name"])

            pelicula = {
                "tmdb_id": datos["id"],
                "titulo": datos["title"],
                "sinopsis": datos["overview"],
                "duracion": datos["runtime"],
                "poster": f"https://image.tmdb.org/t/p/w500{datos['poster_path']}",
                "generos": nombres_generos,
            }
            print(pelicula)
            resultado = agregar_pelicula_db(pelicula)

            respuesta = jsonify(resultado)
        except Exception as e:
            respuesta = jsonify({"Error":str(e)}), 500

    return respuesta

# Endpoint para eliminar peliculas de la base de datos por id
@peliculas_bp.route("/backoffice/eliminar_pelicula_tmdb", methods=["POST"])
def eliminar_pelicula_tmdb():
    id_pelicula = request.json.get("id")
    if not id_pelicula:
        respuesta = jsonify({"Error": "No se envio el campo 'id'"}), 400
    else:
        resultado = eliminar_pelicula_db(id_pelicula)
        respuesta = jsonify(resultado)

    return respuesta