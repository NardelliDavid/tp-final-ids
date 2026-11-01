
from datetime import date
from backend.src.repositories.Carteleras import obtener_cartelera
from backend.src.repositories.Carteleras import obtener_generos_pelicula
from backend.src.repositories.Carteleras import obtener_locales


# GET /cartelera
def listar_cartelera(fecha, local, genero):
    if fecha is None:
        fecha = date.today()

    peliculas = obtener_cartelera(fecha, local, genero)

    respuesta = []

    for pelicula in peliculas:
        datos_generos = obtener_generos_pelicula(pelicula["id"])

        generos = []

        for genero_actual in datos_generos:
            generos.append(genero_actual[0])

        elemento = {
            "id": pelicula["id"],
            "titulo": pelicula["titulo"],
            "poster_url": pelicula["poster_url"],
            "duracion_min": pelicula["duracion_min"],
            "clasificacion": pelicula["clasificacion"],
            "generos": generos
        }

        respuesta.append(elemento)

    return respuesta


# GET /locales
def listar_locales():
    salas = obtener_locales()

    locales = {}

    for sala in salas:
        nombre_local = sala["local"]

        if nombre_local not in locales:
            locales[nombre_local] = {
                "id": nombre_local,
                "nombre": nombre_local,
                "salas": []
            }

        capacidad = sala["filas"] * sala["columnas"]

        datos_sala = {
            "id": sala["id"],
            "nombre": sala["nombre"],
            "filas": sala["filas"],
            "columnas": sala["columnas"],
            "capacidad": capacidad
        }

        locales[nombre_local]["salas"].append(datos_sala)

    respuesta = list(locales.values())

    return respuesta
