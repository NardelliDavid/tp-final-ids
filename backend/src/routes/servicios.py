
from flask import Blueprint, jsonify
from mysql.connector import Error
from src.repositories.servicios_repository import obtener_servicios_activos

servicios_bp = Blueprint("servicios", __name__)

@servicios_bp.route("/servicios", methods=["GET"])
def listar_servicios():
    try:
        servicios = obtener_servicios_activos()

        for servicio in servicios:
            servicio["precio"] = float(servicio["precio"])
            servicio["activo"] = bool(servicio["activo"])

        return jsonify(servicios), 200

    except Error:
        return jsonify({"mensaje": "Error al obtener los servicios"}), 500
