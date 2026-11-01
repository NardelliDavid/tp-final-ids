import requests
from flask import jsonify, Blueprint, request
from ..repositories.dashboard import *

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/backoffice/dashboard", methods=["GET"])
def dashboard_estadisticas():
    contenido, codigo = dashboard_repositories()
    return jsonify(contenido), codigo
