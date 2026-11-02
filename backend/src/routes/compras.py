from datetime import datetime
from flask import Blueprint, jsonify, request
from mysql.connector import Error
from src.routes.perfil import obtener_usuario_autenticado
from src.repositories.compras_repository import (obtener_funcion,butaca_esta_ocupada,registrar_compra,)
from src.repositories.compras_repository import obtener_detalle_compra, cancelar_compra

compras_bp = Blueprint("compras", __name__)

@compras_bp.route("/compras", methods=["POST"])
def crear_compra_endpoint():
    mensaje = None
    respuesta = None
    codigo = 400

    email_usuario = obtener_usuario_autenticado()

    if email_usuario is None:
        mensaje = "No autorizado. Iniciá sesión"
        codigo = 401

    else:
        datos = request.get_json(silent=True)

        if type(datos) != dict:
            mensaje = "JSON inválido"

        else:
            funcion_id = datos.get("funcion_id")
            butacas = datos.get("butacas")
            servicios = datos.get("servicios", [])

            if type(funcion_id) != int or funcion_id <= 0:
                mensaje = "Función inválida"

            elif type(butacas) != list or not (1 <= len(butacas) <= 6):
                mensaje = "Cantidad de butacas inválida"
                codigo = 422

            else:
                try:
                    funcion = obtener_funcion(funcion_id)

                    if funcion is None:
                        mensaje = "Función no encontrada"
                        codigo = 404

                    elif funcion["inicio"] <= datetime.now():
                        mensaje = "La función ya comenzó"
                        codigo = 422

                    else:
                        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                        formato_invalido = False
                        butaca_invalida = False
                        repetidas = False
                        ocupada = False
                        butacas_vistas = []

                        for butaca in butacas:
                            if type(butaca) != str or len(butaca) < 2:
                                formato_invalido = True

                            else:
                                fila = butaca[0]
                                texto_columna = butaca[1:]

                                if (
                                    fila not in letras
                                    or not texto_columna.isascii()
                                    or not texto_columna.isdigit()
                                ):
                                    formato_invalido = True

                                else:
                                    columna = int(texto_columna)

                                    if (
                                        fila not in letras[:funcion["filas"]]
                                        or not (1 <= columna <= funcion["columnas"])
                                    ):
                                        butaca_invalida = True

                                    else:
                                        posicion = (fila, columna)

                                        if posicion in butacas_vistas:
                                            repetidas = True
                                        else:
                                            butacas_vistas.append(posicion)
                                            if butaca_esta_ocupada(funcion_id, fila, columna):
                                                ocupada = True

                        if formato_invalido:
                            mensaje = "Formato de butaca inválido"
                            codigo = 422

                        elif butaca_invalida:
                            mensaje = "Butaca inexistente en la sala"
                            codigo = 422

                        elif repetidas:
                            mensaje = "Hay butacas repetidas"
                            codigo = 422

                        elif ocupada:
                            mensaje = "Una o más butacas están ocupadas"
                            codigo = 409

                        elif type(servicios) != list:
                            mensaje = "Los servicios deben ser una lista"
                            codigo = 422

                        else:
                            servicios_invalidos = False

                            for servicio in servicios:
                                if type(servicio) != dict:
                                    servicios_invalidos = True
                                else:
                                    servicio_id = servicio.get("servicio_id")
                                    cantidad = servicio.get("cantidad")

                                    if (
                                        type(servicio_id) != int
                                        or servicio_id <= 0
                                        or type(cantidad) != int
                                        or not (1 <= cantidad <= 32767)
                                    ):
                                        servicios_invalidos = True

                            if servicios_invalidos:
                                mensaje = "Datos de servicios inválidos"
                                codigo = 422
                            else:
                                respuesta, codigo = registrar_compra(
                                    email_usuario, funcion_id, butacas_vistas, servicios
                                )

                except Error as e:
                    print("ERROR MYSQL:", e)
                    mensaje = "Error al consultar la base de datos"
                    codigo = 500

    if respuesta is None:
        respuesta = {"mensaje": mensaje}

    return jsonify(respuesta), codigo

@compras_bp.route("/compras/<int:id_compra>", methods=["GET"])
def obtener_compra_endpoint(id_compra):

    email_usuario = obtener_usuario_autenticado()

    if email_usuario is None:
        return jsonify({"mensaje": "No autorizado. Iniciá sesión"}), 401

    if id_compra <= 0:
        return jsonify({"mensaje": "Compra inválida"}), 400

    try:
        respuesta, codigo = obtener_detalle_compra(id_compra, email_usuario)
        return jsonify(respuesta), codigo

    except Exception:
        return jsonify({"mensaje": "Error interno del servidor"}), 500

@compras_bp.route("/compras/<int:id_compra>/cancelacion", methods=["POST"])
def cancelar_compra_endpoint(id_compra):

    email_usuario = obtener_usuario_autenticado()

    if email_usuario is None:
        return jsonify({"mensaje": "No autorizado. Iniciá sesión"}), 401

    if id_compra <= 0:
        return jsonify({"mensaje": "Compra inválida"}), 400

    try:
        respuesta, codigo = cancelar_compra(id_compra, email_usuario)
        return jsonify(respuesta), codigo

    except Exception:

        return jsonify({"mensaje": "Error interno del servidor"}), 500