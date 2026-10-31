from flask import Blueprint, jsonify
from backend.src.services.Funciones import obtener_butacas_funcion


funciones_bp = Blueprint("funciones", __name__)

# GET /funciones/{id}/butacas
@funciones_bp.route("/funciones/<int:funcion_id>/butacas", methods=["GET"])
def obtener_butacas(funcion_id):

    # Obtiene el mapa de butacas de una función.
    respuesta = obtener_butacas_funcion(funcion_id)

    if respuesta is None:
        return jsonify({"error": "La función no existe"}), 404

    return jsonify(respuesta), 200