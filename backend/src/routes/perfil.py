from flask import Blueprint, jsonify, request
from src.services.validar import verificar_token
from src.services.perfil import (
    consultar_datos_perfil,
    actualizar_datos_perfil,
    consultar_historial_usuario
)
# Mantiene compatibilidad con QR.py que importa esta función desde acá
def obtener_usuario_autenticado():
    return verificar_token(request.headers.get('Authorization'))


# Crea el Blueprint exclusivo para el módulo de Perfil
perfil_bp = Blueprint('perfil', __name__)


# endpoint GET /usuarios/me  Obtener los datos del perfil del usuario actual
@perfil_bp.route('/usuarios/me', methods=['GET'])
def obtener_perfil():
    # Valida que el cliente tenga un token real y activo
    email_usuario = verificar_token(request.headers.get('Authorization'))
    if not email_usuario:
        return jsonify({"mensaje": "Token inválido o inexistente. No autorizado."}), 401

    respuesta, status_code = consultar_datos_perfil(email_usuario)
    return jsonify(respuesta), status_code


# endpoint PATCH /usuarios/me  Modificar campos editables (nombre o contraseña)
@perfil_bp.route('/usuarios/me', methods=['PATCH'])
def modificar_perfil():
    # Verifica autenticación
    email_usuario = verificar_token(request.headers.get('Authorization'))
    if not email_usuario:
        return jsonify({"mensaje": "No autorizado"}), 401

    datos = request.get_json() or {}
    nombre_nuevo = datos.get('nombre')
    pwd_actual = datos.get('password_actual')
    pwd_nueva = datos.get('password_nueva')

    respuesta, status_code = actualizar_datos_perfil(
        email_usuario, nombre_nuevo, pwd_actual, pwd_nueva
    )
    return jsonify(respuesta), status_code


# endpoint GET /usuarios/me/historial  Reunir compras y películas vistas
@perfil_bp.route('/usuarios/me/historial', methods=['GET'])
def obtener_historial():
    # Verificamos autenticación
    email_usuario = verificar_token(request.headers.get('Authorization'))
    if not email_usuario:
        return jsonify({"mensaje": "No autorizado"}), 401

    respuesta, status_code = consultar_historial_usuario(email_usuario)
    return jsonify(respuesta), status_code
