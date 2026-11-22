from flask import Blueprint, jsonify, request
from src.services.Carteleras import listar_cartelera
from src.services.Carteleras import listar_locales
from src.validators.Carteleras import validar_consulta_locales
from src.services.Carteleras import listar_funciones_pelicula

carteleras_bp = Blueprint("carteleras", __name__)


# GET /cartelera
@carteleras_bp.route("/cartelera", methods=["GET"])
def obtener_cartelera():
    respuesta = listar_cartelera()

    return jsonify(respuesta), 200


# GET /locales
@carteleras_bp.route("/locales", methods=["GET"])
def obtener_locales():
    parametros = request.args

    if not validar_consulta_locales(parametros):
        return jsonify({
            "error": "Este endpoint no acepta parámetros"
        }), 422

    respuesta = listar_locales()

    return jsonify(respuesta), 200


# GET /peliculas/<id>/funciones
@carteleras_bp.route("/peliculas/<int:pelicula_id>/funciones", methods=["GET"])
def obtener_funciones_pelicula(pelicula_id):
    respuesta = listar_funciones_pelicula(pelicula_id)

    if respuesta is None:
        return jsonify({"error": "La película no existe"}), 404

    return jsonify(respuesta), 200