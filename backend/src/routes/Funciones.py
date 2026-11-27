from flask import Blueprint, jsonify, request
from db.conexion_db import conexion
from src.routes.perfil import obtener_usuario_autenticado
from src.services.Funciones import obtener_butacas_funcion
from src.services.Funciones import eliminar_funcion
from src.services.Funciones import actualizar_funcion
from src.services.Funciones import crear_funcion
from src.services.Funciones import obtener_detalle_funcion_servicio
from src.services.Funciones import listar_funciones
from src.validators.Funciones import validar_filtros_funciones
from src.repositories.Funciones import obtener_salas


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

# GET /salas
@funciones_bp.route("/salas", methods=["GET"])
def listar_salas():
    if not verificar_administrador():
        return jsonify({"error": "No autorizado"}), 401

    salas = obtener_salas()

    return jsonify(salas), 200


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


# GET /funciones/{id}
@funciones_bp.route("/funciones/<int:funcion_id>", methods=["GET"])
def detalle_funcion(funcion_id):
    respuesta = obtener_detalle_funcion_servicio(funcion_id)

    if respuesta is None:
        return jsonify({"error": "La función no existe"}), 404

    return jsonify(respuesta), 200


# GET /funciones/{id}/butacas
@funciones_bp.route("/funciones/<int:funcion_id>/butacas", methods=["GET"])
def obtener_butacas(funcion_id):
    respuesta = obtener_butacas_funcion(funcion_id)

    if respuesta is None:
        return jsonify({"error": "La función no existe"}), 404

    return jsonify(respuesta), 200


# POST /funciones
@funciones_bp.route("/funciones", methods=["POST"])
def registrar_funcion():
    if not verificar_administrador():
        return jsonify({"error": "No autorizado"}), 401

    datos = request.get_json(silent=True)

    respuesta, codigo = crear_funcion(datos)

    if codigo == 404:
        return jsonify(respuesta), 404

    if codigo == 422:
        return jsonify(respuesta), 422

    return jsonify(respuesta), 201


# PATCH /funciones/{id}
@funciones_bp.route("/funciones/<int:funcion_id>", methods=["PATCH"])
def modificar_funcion(funcion_id):
    if not verificar_administrador():
        return jsonify({"error": "No autorizado"}), 401

    datos = request.get_json(silent=True)

    respuesta, codigo = actualizar_funcion(funcion_id, datos)

    if codigo == 404:
        return jsonify({"error": "La función no existe"}), 404

    if codigo == 409:
        return jsonify({"error": "La función tiene compras activas"}), 409

    if codigo == 422:
        return jsonify({"error": respuesta}), 422

    return jsonify(respuesta), 200


# DELETE /funciones/{id}
@funciones_bp.route("/funciones/<int:funcion_id>", methods=["DELETE"])
def eliminar_funcion_ruta(funcion_id):
    if not verificar_administrador():
        return jsonify({"error": "No autorizado"}), 401

    respuesta = eliminar_funcion(funcion_id)

    if respuesta == 404:
        return jsonify({"error": "La función no existe"}), 404

    if respuesta == 409:
        return jsonify({
            "error": "La función tiene entradas asociadas y no puede eliminarse"
        }), 409

    return "", 204
