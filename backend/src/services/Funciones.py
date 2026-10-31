from backend.src.repositories.Funciones import obtener_datos_butacas

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