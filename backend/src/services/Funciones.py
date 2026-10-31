from datetime import datetime, timedelta
from backend.src.repositories.Funciones import obtener_datos_butacas
from backend.src.repositories.Funciones import dar_de_baja_funcion as dar_de_baja_funcion_db
from backend.src.repositories.Funciones import tiene_compras_activas
from backend.src.repositories.Funciones import obtener_funcion_por_id
from backend.src.repositories.Funciones import actualizar_funcion as actualizar_funcion_db
from backend.src.repositories.Funciones import obtener_duracion_pelicula
from backend.src.repositories.Funciones import existe_sala
from backend.src.repositories.Funciones import existe_superposicion
from backend.src.repositories.Funciones import crear_funcion as crear_funcion_db
from backend.src.repositories.Funciones import obtener_detalle_funcion


#GET/funciones/{id}
def obtener_detalle_funcion_servicio(funcion_id):
    respuesta = obtener_detalle_funcion(funcion_id)

    if respuesta is not None:
        respuesta["precio"] = float(respuesta["precio"])
        respuesta["inicio"] = respuesta["inicio"].isoformat()

    return respuesta


# GET /funciones/{id}/butacas
def obtener_butacas_funcion(funcion_id):
    respuesta = None

    datos = obtener_datos_butacas(funcion_id)

    if datos is not None:
        filas = datos["filas"]
        columnas = datos["columnas"]
        ocupadas = datos["ocupadas"]

        butacas = []

        for fila in range(1, filas + 1):
            for numero in range(1, columnas + 1):
                letra_fila = chr(64 + fila)

                if any(
                    entrada["fila"] == fila and entrada["columna"] == numero
                    for entrada in ocupadas
                ):
                    estado = "ocupada"
                else:
                    estado = "libre"

                butaca = {
                    "codigo": letra_fila + str(numero),
                    "fila": letra_fila,
                    "numero": numero,
                    "estado": estado
                }

                butacas.append(butaca)

        respuesta = {
            "funcion_id": funcion_id,
            "filas": filas,
            "columnas": columnas,
            "butacas": butacas
        }

    return respuesta

# POST/funciones 
def crear_funcion(datos):
    respuesta = {}
    codigo = 201

    if not isinstance(datos, dict):
        respuesta = {"error": "Los datos enviados no son válidos"}
        codigo = 422

    elif (
        "pelicula_id" not in datos
        or "sala_id" not in datos
        or "inicio" not in datos
        or "precio" not in datos
    ):
        respuesta = {"error": "Faltan datos obligatorios"}
        codigo = 422

    else:
        pelicula_id = datos["pelicula_id"]
        sala_id = datos["sala_id"]
        inicio_texto = datos["inicio"]
        precio = datos["precio"]

        if (
            not isinstance(pelicula_id, int)
            or isinstance(pelicula_id, bool)
            or pelicula_id <= 0
            or not isinstance(sala_id, int)
            or isinstance(sala_id, bool)
            or sala_id <= 0
            or not isinstance(inicio_texto, str)
            or not isinstance(precio, (int, float))
            or isinstance(precio, bool)
            or precio <= 0
        ):
            respuesta = {"error": "Los datos enviados no son válidos"}
            codigo = 422

        else:
            try:
                inicio = datetime.fromisoformat(inicio_texto)
            except ValueError:
                inicio = None

            if inicio is None:
                respuesta = {"error": "El formato de fecha es incorrecto"}
                codigo = 422

            elif inicio <= datetime.now():
                respuesta = {"error": "La función no puede programarse en el pasado"}
                codigo = 422

            else:
                pelicula = obtener_duracion_pelicula(pelicula_id)

                if pelicula is None:
                    respuesta = {"error": "La película no existe"}
                    codigo = 404

                elif not existe_sala(sala_id):
                    respuesta = {"error": "La sala no existe"}
                    codigo = 404

                else:
                    duracion = pelicula["duracion_min"]
                    fin = inicio + timedelta(minutes=duracion)

                    if existe_superposicion(sala_id, inicio, fin):
                        respuesta = {
                            "error": "La sala tiene otra función en ese horario o no cumple los 20 minutos de limpieza"
                        }
                        codigo = 422

                    else:
                        funcion_id = crear_funcion_db(
                            pelicula_id,
                            sala_id,
                            inicio,
                            fin,
                            precio
                        )

                        respuesta = {
                            "mensaje": "Función creada correctamente",
                            "funcion_id": funcion_id,
                            "pelicula_id": pelicula_id,
                            "sala_id": sala_id,
                            "inicio": inicio.isoformat(),
                            "fin": fin.isoformat(),
                            "precio": precio
                        }

    return respuesta, codigo



# PATCH	/funciones/{id}
def actualizar_funcion(funcion_id, datos):
    respuesta = {}
    codigo = 200

    funcion = obtener_funcion_por_id(funcion_id)

    if funcion is None:
        respuesta = {"error": "La función no existe"}
        codigo = 404

    elif datos is None or not isinstance(datos, dict):
        respuesta = {"error": "Los datos enviados no son válidos"}
        codigo = 422

    elif len(datos) == 0 or any(
        campo not in ["sala_id", "inicio", "precio"]
        for campo in datos
    ):
        respuesta = {"error": "Solo se pueden modificar sala_id, inicio y precio"}
        codigo = 422

    else:
        sala_id = datos.get("sala_id", funcion["sala_id"])
        inicio = datos.get("inicio", funcion["inicio"])
        precio = datos.get("precio", funcion["precio"])

        if isinstance(inicio, str):
            try:
                inicio = datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                inicio = None

        if (
            not isinstance(sala_id, int)
            or sala_id <= 0
            or inicio is None
            or precio <= 0
        ):
            respuesta = {"error": "Los datos enviados no son válidos"}
            codigo = 422

        else:
            respuesta = {
                "id": funcion_id,
                "sala_id": sala_id,
                "inicio": inicio.strftime("%Y-%m-%d %H:%M:%S"),
                "precio": float(precio)
            }

            codigo = 200

    return respuesta, codigo


# DELETE/funciones/{id} 
def dar_de_baja_funcion(funcion_id):
    respuesta = 204

    datos = obtener_datos_butacas(funcion_id)

    if datos is None:
        respuesta = 404

    else:
        if tiene_compras_activas(funcion_id):
            respuesta = 409

        else:
            dar_de_baja_funcion_db(funcion_id)

    return respuesta