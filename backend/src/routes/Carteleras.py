
from flask import Blueprint, jsonify, request
from src.services.Cartelera import listar_cartelera
from src.services.Cartelera import listar_locales
from src.validators.Carteleras import validar_filtros_cartelera
from src.validators.Carteleras import validar_consulta_locales

carteleras_bp = Blueprint("carteleras", __name__)


# GET /cartelera
@carteleras_bp.route("/cartelera", methods=["GET"])
def obtener_cartelera():
    filtros = {}

    parametros = ["fecha", "local", "genero"]

    for parametro in parametros:
        valor = request.args.get(parametro)

        if valor is not None:
            filtros[parametro] = valor

    if not validar_filtros_cartelera(filtros):
        return jsonify({
            "error": "Los filtros enviados no son válidos"
        }), 422

    fecha = filtros.get("fecha")
    local = filtros.get("local")
    genero = filtros.get("genero")

    respuesta = listar_cartelera(fecha, local, genero)

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
