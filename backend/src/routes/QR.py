from flask import Blueprint, jsonify, request
from db.conexion_db import conexion
from itsdangerous import URLSafeTimedSerializer, BadSignature

qr_bp = Blueprint("qr", __name__)

serializador = URLSafeTimedSerializer("mi_clave_segura")


@qr_bp.route("/qr/validar", methods=["POST"])
def validar_qr():

    # Verificar que el usuario haya iniciado sesión
    autorizacion = request.headers.get("Authorization", "")

    if not autorizacion.startswith("Bearer "):
        return jsonify({"mensaje": "Debes iniciar sesión"}), 401

    token = autorizacion.replace("Bearer ", "", 1)

    try:
        email = serializador.loads(token, salt="auth-salt")
    except BadSignature:
        return jsonify({"mensaje": "Token inválido"}), 401

    conn = conexion()
    cursor = conn.cursor()

    try:
        # Verificar que el usuario sea administrador
        cursor.execute(
            "SELECT rol FROM usuarios WHERE email = %s",
            (email,)
        )
        usuario = cursor.fetchone()

        if not usuario or usuario[0] != "administrador":
            return jsonify({"mensaje": "Acceso denegado"}), 403

        datos = request.get_json() or {}
        codigo_qr = datos.get("codigo_qr")

        if not codigo_qr:
            return jsonify({"mensaje": "Falta el código QR"}), 400

        # Buscar la compra
        cursor.execute(
            "SELECT id, estado FROM compras WHERE codigo_qr = %s FOR UPDATE",
            (codigo_qr,)
        )
        compra = cursor.fetchone()

        if not compra:
            conn.rollback()
            return jsonify({"mensaje": "QR no encontrado"}), 404

        compra_id, estado = compra

        if estado != "activa":
            conn.rollback()
            return jsonify({"mensaje": "La compra ya fue utilizada o está cancelada"}), 400

        # Comprobar que existan entradas activas
        cursor.execute(
            "SELECT COUNT(*) FROM entradas WHERE compra_id = %s AND estado = 'activa'",
            (compra_id,)
        )
        cantidad = cursor.fetchone()[0]

        if cantidad == 0:
            conn.rollback()
            return jsonify({"mensaje": "La compra no tiene entradas activas"}), 400

        # Marcar la compra y sus entradas como utilizadas
        cursor.execute(
            "UPDATE compras SET estado = 'utilizada' WHERE id = %s",
            (compra_id,)
        )

        cursor.execute(
            "UPDATE entradas SET estado = 'utilizada' WHERE compra_id = %s AND estado = 'activa'",
            (compra_id,)
        )

        conn.commit()

        return jsonify({
            "mensaje": "QR validado correctamente",
            "entradas_utilizadas": cantidad
        }), 200

    except Exception:
        conn.rollback()
        return jsonify({"mensaje": "Error al validar el QR"}), 500

    finally:
        cursor.close()
        conn.close()