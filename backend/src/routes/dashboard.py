import requests
from flask import jsonify, Blueprint, request
from ..repositories.dashboard import *
from ..repositories.peliculas import es_admin
from src.routes.perfil import obtener_usuario_autenticado

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/backoffice/dashboard", methods=["GET"])
def dashboard_estadisticas():
    email_usuario = obtener_usuario_autenticado()

    if email_usuario is None:
        respuesta = jsonify({"Error":"Debe iniciar sesion como administrador."}), 401
    else:
        usuario_es_admin = es_admin(email_usuario)
        if not usuario_es_admin:
            respuesta = jsonify({"Error":"Usted no es administrador"}), 403
        else:
            contenido, codigo = dashboard_repositories()
            respuesta = jsonify(contenido), codigo
    return respuesta
