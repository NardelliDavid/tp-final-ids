from flask import Blueprint, jsonify, request
from backend.src.services.Funciones import obtener_butacas_funcion
from backend.src.services.Funciones import dar_de_baja_funcion
from backend.src.services.Funciones import actualizar_funcion

funciones_bp = Blueprint("funciones", __name__)

# GET /funciones/{id}/butacas
@funciones_bp.route("/funciones/<int:funcion_id>/butacas", methods=["GET"])
def obtener_butacas(funcion_id):

    # Obtiene el mapa de butacas de una función.
    respuesta = obtener_butacas_funcion(funcion_id)

    if respuesta is None:
        return jsonify({"error": "La función no existe"}), 404

    return jsonify(respuesta), 200

# PATCH	/funciones/{id}
@funciones_bp.route("/funciones/<int:funcion_id>", methods=["PATCH"])
def modificar_funcion(funcion_id):
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

    respuesta = dar_de_baja_funcion(funcion_id)

    if respuesta == 404:
        return jsonify({"error": "La función no existe"}), 404

    if respuesta == 409:
        return jsonify({"error": "La función tiene compras activas"}), 409

    return "", 204
