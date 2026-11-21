from flask import Blueprint, jsonify, request
from src.services.validar import registrar_usuario, autenticar_usuario

auth_bp = Blueprint('auth', __name__)


# Endpoint de Registro
@auth_bp.route('/auth/registro', methods=['POST'])
def registro():
    datos = request.get_json() or {}
    nombre = datos.get('nombre')
    email = datos.get('email')
    password = datos.get('password')

    if not nombre or not email or not password:
        return jsonify({"mensaje": "Faltan datos obligatorios"}), 400

    respuesta, status_code = registrar_usuario(nombre, email, password)
    return jsonify(respuesta), status_code


# Endpoint de Login
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    datos = request.get_json() or {}
    email = datos.get('email')
    password = datos.get('password')

    if not email or not password:
        return jsonify({"mensaje": "Faltan datos obligatorios"}), 400

    respuesta, status_code = autenticar_usuario(email, password)
    return jsonify(respuesta), status_code
