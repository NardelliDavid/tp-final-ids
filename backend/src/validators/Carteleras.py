
from datetime import datetime


# GET /cartelera
def validar_filtros_cartelera(filtros):
    respuesta = True

    campos_permitidos = ["fecha", "local", "genero"]

    for campo in filtros:
        if campo not in campos_permitidos:
            respuesta = False

    if "fecha" in filtros:
        try:
            datetime.strptime(filtros["fecha"], "%Y-%m-%d")
        except ValueError:
            respuesta = False

    if "local" in filtros:
        if len(filtros["local"].strip()) == 0:
            respuesta = False

    if "genero" in filtros:
        if len(filtros["genero"].strip()) == 0:
            respuesta = False

    return respuesta


# GET /locales
def validar_consulta_locales(parametros):
    respuesta = True

    if len(parametros) > 0:
        respuesta = False

    return respuesta
