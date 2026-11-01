from flask import Blueprint, jsonify, request
from db.conexion_db import conexion
from src.routes.perfil import obtener_usuario_autenticado
from src.services.funciones import obtener_butacas_funcion
from src.services.funciones import dar_de_baja_funcion
from src.services.funciones import actualizar_funcion
from src.services.funciones import crear_funcion
from src.services.funciones import obtener_detalle_funcion_servicio
from src.services.funciones import listar_funciones
from src.validators.Funciones import validar_filtros_funciones

funciones_bp = Blueprint("funciones", __name__)

# Verificar que el usuario sea administrador
def verificar_administrador():
    email_usuario = obtener_usuario_autenticado()

    respuesta = None
    codigo = 200

    if email_usuario is None:
        respuesta = "Debes iniciar sesión"
        codigo = 401

    else:
        conn = conexion()
        cursor = conn.cursor()

        consulta = """
            SELECT rol
            FROM usuarios
            WHERE email = %s
        """

        cursor.execute(consulta, (email_usuario,))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario is None:
            respuesta = "Usuario no encontrado"
            codigo = 401

        elif usuario[0] != "administrador":
            respuesta = "No tienes permisos para realizar esta operación"
            codigo = 403

    return respuesta, codigo

# GET /funciones
@funciones_bp.route("/funciones", methods=["GET"])
def obtener_funciones():
    filtros = {}

    parametros = [
        "pelicula_id",
        "sala_id",
        "fecha",
        "desde",
        "hasta"
    ]

    for parametro in parametros:
        valor = request.args.get(parametro)

        if valor is not None:
            filtros[parametro] = valor

    if not validar_filtros_funciones(filtros):
        return jsonify({"error": "Los filtros enviados no son válidos"}), 422

    incluir_pasadas = request.args.get(
        "incluir_pasadas", "false"
    ).lower() == "true"

    respuesta = listar_funciones(filtros, incluir_pasadas)

    return jsonify(respuesta), 200

#GET/funciones/{id}
@funciones_bp.route("/funciones/<int:funcion_id>", methods=["GET"])
def detalle_funcion(funcion_id):
    respuesta = obtener_detalle_funcion_servicio(funcion_id)

    if respuesta is None:
        return jsonify({"error": "La función no existe"}), 404

    return jsonify(respuesta), 200


# GET /funciones/{id}/butacas
@funciones_bp.route("/funciones/<int:funcion_id>/butacas", methods=["GET"])
def obtener_butacas(funcion_id):

    # Obtiene el mapa de butacas de una función.
    respuesta = obtener_butacas_funcion(funcion_id)

    if respuesta is None:
        return jsonify({"error": "La función no existe"}), 404

    return jsonify(respuesta), 200

# POST/funciones 
@funciones_bp.route("/funciones", methods=["POST"])
def registrar_funcion():
    mensaje, codigo = verificar_administrador()

    if codigo != 200:
        return jsonify({"error": mensaje}), codigo

    datos = request.get_json(silent=True)

    respuesta, codigo = crear_funcion(datos)

    if codigo == 404:
        return jsonify(respuesta), 404

    if codigo == 422:
        return jsonify(respuesta), 422

    return jsonify(respuesta), 201


# PATCH	/funciones/{id}
@funciones_bp.route("/funciones/<int:funcion_id>", methods=["PATCH"])
def modificar_funcion(funcion_id):
    
    mensaje, codigo = verificar_administrador()

    if codigo != 200:
        return jsonify({"error": mensaje}), codigo
    datos = request.get_json(silent=True)

    respuesta, codigo = actualizar_funcion(funcion_id, datos)

    if codigo == 404:
        return jsonify({"error": "La función no existe"}), 404

    if codigo == 409:
        return jsonify({"error": "La función tiene compras activas"}), 409

    if codigo == 422:
        return jsonify({"error": respuesta}), 422

    return jsonify(respuesta), 200


# DELETE/funciones/{id} 
@funciones_bp.route("/funciones/<int:funcion_id>", methods=["DELETE"])
def eliminar_funcion(funcion_id):
    mensaje, codigo = verificar_administrador()

    if codigo != 200:
        return jsonify({"error": mensaje}), codigo

    respuesta = dar_de_baja_funcion(funcion_id)

    if respuesta == 404:
        return jsonify({"error": "La función no existe"}), 404

    if respuesta == 409:
        return jsonify({"error": "La función tiene compras activas"}), 409

    return "", 204
