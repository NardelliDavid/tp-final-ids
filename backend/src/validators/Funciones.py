from datetime import datetime

#GET/funciones/
def validar_filtros_funciones(filtros):
    respuesta = True

    campos_permitidos = [
        "pelicula_id",
        "sala_id",
        "fecha",
        "desde",
        "hasta"
    ]

    for campo in filtros:
        if campo not in campos_permitidos:
            respuesta = False

    if "pelicula_id" in filtros:
        if not filtros["pelicula_id"].isdecimal():
            respuesta = False
        elif int(filtros["pelicula_id"]) <= 0:
            respuesta = False

    if "sala_id" in filtros:
        if not filtros["sala_id"].isdecimal():
            respuesta = False
        elif int(filtros["sala_id"]) <= 0:
            respuesta = False

    if "fecha" in filtros:
        try:
            datetime.strptime(filtros["fecha"], "%Y-%m-%d")
        except ValueError:
            respuesta = False

    if "desde" in filtros:
        try:
            datetime.strptime(filtros["desde"], "%Y-%m-%d")
        except ValueError:
            respuesta = False

    if "hasta" in filtros:
        try:
            datetime.strptime(filtros["hasta"], "%Y-%m-%d")
        except ValueError:
            respuesta = False

    if "desde" in filtros and "hasta" not in filtros:
        respuesta = False

    if "hasta" in filtros and "desde" not in filtros:
        respuesta = False

    if "fecha" in filtros and (
        "desde" in filtros or "hasta" in filtros
    ):
        respuesta = False

    if "desde" in filtros and "hasta" in filtros:
        if filtros["desde"] > filtros["hasta"]:
            respuesta = False

    return respuesta

# POST /funciones
def validar_datos_funcion(datos):
    respuesta = True

    if not isinstance(datos, dict):
        respuesta = False
    else:
        campos_obligatorios = [
            "pelicula_id",
            "sala_id",
            "inicio",
            "precio"
        ]

        for campo in campos_obligatorios:
            if campo not in datos:
                respuesta = False

        if respuesta:
            if (
                not isinstance(datos["pelicula_id"], int)
                or isinstance(datos["pelicula_id"], bool)
                or datos["pelicula_id"] <= 0
            ):
                respuesta = False

            if (
                not isinstance(datos["sala_id"], int)
                or isinstance(datos["sala_id"], bool)
                or datos["sala_id"] <= 0
            ):
                respuesta = False

            if not isinstance(datos["inicio"], str):
                respuesta = False
            else:
                try:
                    datetime.fromisoformat(datos["inicio"])
                except ValueError:
                    respuesta = False

            if (
                not isinstance(datos["precio"], (int, float))
                or isinstance(datos["precio"], bool)
                or datos["precio"] <= 0
            ):
                respuesta = False

    return respuesta

# PATCH	/funciones/{id}
def validar_datos_actualizacion(datos):
    respuesta = True

    if not isinstance(datos, dict) or len(datos) == 0:
        respuesta = False

    else:
        campos_permitidos = ["sala_id", "inicio", "precio"]

        for campo in datos:
            if campo not in campos_permitidos:
                respuesta = False

        if "sala_id" in datos:
            if not isinstance(datos["sala_id"], int) or datos["sala_id"] <= 0:
                respuesta = False

        if "inicio" in datos:
            if not isinstance(datos["inicio"], str):
                respuesta = False
            else:
                try:
                    datetime.strptime(datos["inicio"], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    respuesta = False

        if "precio" in datos:
            if (
                not isinstance(datos["precio"], (int, float))
                or isinstance(datos["precio"], bool)
                or datos["precio"] <= 0
            ):
                respuesta = False

    return respuesta