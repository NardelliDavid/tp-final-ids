from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from db.conexion_db import conexion
from src.routes.perfil import obtener_usuario_autenticado

qr_bp = Blueprint("qr", __name__)


def error(mensaje, codigo, status):
    return jsonify({"mensaje": mensaje, "codigo": codigo}), status


@qr_bp.route("/qr/validaciones", methods=["POST"])
def validar_qr():
    email = obtener_usuario_autenticado()
    if email is None:
        return jsonify({"mensaje": "No autorizado. Iniciá sesión"}), 401

    datos = request.get_json(silent=True)
    if type(datos) != dict:
        return jsonify({"mensaje": "JSON inválido"}), 400

    token = datos.get("token")
    funcion_id = datos.get("funcion_id")
    if type(token) != str or not token.strip():
        return jsonify({"mensaje": "Falta el token del QR"}), 400
    if type(funcion_id) != int or funcion_id <= 0:
        return jsonify({"mensaje": "Falta la función"}), 400
    token = token.strip()

    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Solo administradores
        cursor.execute("SELECT rol FROM usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        if not usuario or usuario["rol"] != "administrador":
            return jsonify({"mensaje": "Acceso denegado"}), 403

        # 2. El token existe (se bloquea la compra mientras se valida)
        cursor.execute(
            "SELECT c.id, c.estado, u.nombre AS cliente "
            "FROM compras c JOIN usuarios u ON u.id = c.usuario_id "
            "WHERE c.codigo_qr = %s FOR UPDATE",
            (token,)
        )
        compra = cursor.fetchone()
        if not compra:
            conn.rollback()
            return error("QR inexistente", "QR_INEXISTENTE", 404)

        # 3. No cancelada ni utilizada
        if compra["estado"] == "cancelada":
            conn.rollback()
            return error("La compra está cancelada", "QR_CANCELADO", 409)
        if compra["estado"] == "utilizada":
            conn.rollback()
            return error("El QR ya fue utilizado", "QR_UTILIZADO", 409)

        # 4. Corresponde a la función que se controla
        cursor.execute(
            "SELECT f.inicio, p.titulo, s.local, s.nombre AS sala "
            "FROM entradas e "
            "JOIN funciones f ON f.id = e.funcion_id "
            "JOIN peliculas p ON p.id = f.pelicula_id "
            "JOIN salas s ON s.id = f.sala_id "
            "WHERE e.compra_id = %s AND e.funcion_id = %s LIMIT 1",
            (compra["id"], funcion_id)
        )
        funcion = cursor.fetchone()
        if not funcion:
            conn.rollback()
            return error("El QR es de otra función", "FUNCION_INCORRECTA", 422)

        # 5. Ventana: 60 min antes hasta 30 min después del inicio
        ahora = datetime.now()
        inicio = funcion["inicio"]
        if ahora < inicio - timedelta(minutes=60) or ahora > inicio + timedelta(minutes=30):
            conn.rollback()
            return error("Fuera del horario de ingreso", "FUERA_DE_VENTANA", 422)

        # 6. Marcar utilizada (solo si sigue activa)
        cursor.execute(
            "UPDATE compras SET estado = 'utilizada' "
            "WHERE id = %s AND estado = 'activa'",
            (compra["id"],)
        )
        if cursor.rowcount == 0:
            conn.rollback()
            return error("El QR ya fue utilizado", "QR_UTILIZADO", 409)

        cursor.execute(
            "UPDATE entradas SET estado = 'utilizada' "
            "WHERE compra_id = %s AND estado = 'activa'",
            (compra["id"],)
        )

        cursor.execute(
            "SELECT fila, columna FROM entradas "
            "WHERE compra_id = %s ORDER BY fila, columna",
            (compra["id"],)
        )
        butacas = [{"fila": b["fila"], "columna": b["columna"]} for b in cursor.fetchall()]

        conn.commit()

        return jsonify({
            "valido": True,
            "mensaje": "QR validado correctamente",
            "compra_id": compra["id"],
            "cliente": compra["cliente"],
            "pelicula": funcion["titulo"],
            "sala": funcion["sala"],
            "inicio": inicio.isoformat(),
            "butacas": butacas,
            "validada_en": ahora.isoformat(timespec="seconds")
        }), 200

    except Exception:
        conn.rollback()
        return jsonify({"mensaje": "Error al validar el QR"}), 500

    finally:
        cursor.close()
        conn.close()