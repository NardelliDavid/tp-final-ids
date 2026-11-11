from flask import Blueprint, jsonify, request
from mysql.connector import Error
from db.conexion_db import conexion
from src.routes.perfil import obtener_usuario_autenticado
from src.repositories.servicios_repository import (
    obtener_servicios_activos,
    crear_servicio,
    modificar_servicio,
    eliminar_servicio
)

servicios_bp = Blueprint("servicios", __name__)


# Verificar que el usuario sea administrador
def verificar_administrador():
    email = obtener_usuario_autenticado()

    if not email:
        return jsonify({
            "mensaje": "No autorizado. Token inválido o inexistente"
        }), 401

    conn = None
    cursor = None

    try:
        conn = conexion()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT rol FROM usuarios WHERE email = %s",
            (email,)
        )

        usuario = cursor.fetchone()

        if not usuario or usuario[0] != "administrador":
            return jsonify({
                "mensaje": "Acceso permitido solo a administradores"
            }), 403

    except Error:
        return jsonify({
            "mensaje": "Error al verificar los permisos"
        }), 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

    return None


# Obtener los servicios activos
@servicios_bp.route("/servicios", methods=["GET"])
def listar_servicios():
    try:
        servicios = obtener_servicios_activos()

        for servicio in servicios:
            servicio["precio"] = float(servicio["precio"])
            servicio["activo"] = bool(servicio["activo"])

        return jsonify(servicios), 200

    except Error:
        return jsonify({
            "mensaje": "Error al obtener los servicios"
        }), 500


# Crear un nuevo servicio
@servicios_bp.route("/servicios", methods=["POST"])
def agregar_servicio():

    # Comprobar permisos
    error = verificar_administrador()
    if error is not None:
        return error

    datos = request.get_json(silent=True)

    if type(datos) != dict:
        return jsonify({"mensaje": "JSON inválido"}), 400

    nombre = datos.get("nombre")
    descripcion = datos.get("descripcion")
    precio = datos.get("precio")

    # Validar datos obligatorios
    if nombre is None or precio is None:
        return jsonify({"mensaje": "Faltan datos obligatorios"}), 400

    # Validar nombre
    if type(nombre) != str or nombre.strip() == "":
        return jsonify({"mensaje": "Nombre inválido"}), 400

    # Validar precio
    if type(precio) not in (int, float) or precio <= 0:
        return jsonify({"mensaje": "Precio inválido"}), 400

    nombre = nombre.strip()

    try:
        id_servicio = crear_servicio(nombre, descripcion, precio)

        return jsonify({
            "mensaje": "Servicio creado correctamente",
            "id": id_servicio
        }), 201

    except Error:
        return jsonify({
            "mensaje": "Error al crear el servicio"
        }), 500


# Modificar un servicio
@servicios_bp.route("/servicios/<int:id_servicio>", methods=["PATCH"])
def modificar_servicio_endpoint(id_servicio):

    # Comprobar permisos
    error = verificar_administrador()
    if error is not None:
        return error

    datos = request.get_json(silent=True)

    mensaje = None
    codigo = 400

    if type(datos) != dict or not datos:
        mensaje = "JSON inválido o vacío"

    else:
        permitidos = ("nombre", "descripcion", "precio")

        # Validar campos permitidos
        for campo in datos:
            if campo not in permitidos:
                mensaje = "Campo no permitido"

        # Validar nombre
        if mensaje is None and "nombre" in datos:
            nombre = datos["nombre"]

            if type(nombre) != str or nombre.strip() == "":
                mensaje = "Nombre inválido"
            else:
                datos["nombre"] = nombre.strip()

        # Validar precio
        if mensaje is None and "precio" in datos:
            precio = datos["precio"]

            if type(precio) not in (int, float) or precio <= 0:
                mensaje = "Precio inválido"

        # Validar descripción
        if mensaje is None and "descripcion" in datos:
            descripcion = datos["descripcion"]

            if descripcion is not None and type(descripcion) != str:
                mensaje = "Descripción inválida"

        # Modificar servicio
        if mensaje is None:
            try:
                modificado = modificar_servicio(id_servicio, datos)

                if modificado:
                    mensaje = "Servicio modificado correctamente"
                    codigo = 200
                else:
                    mensaje = "Servicio no encontrado"
                    codigo = 404

            except Error:
                mensaje = "Error al modificar el servicio"
                codigo = 500

    return jsonify({"mensaje": mensaje}), codigo


# Eliminar un servicio (baja lógica)
@servicios_bp.route("/servicios/<int:id_servicio>", methods=["DELETE"])
def eliminar_servicio_endpoint(id_servicio):

    # Comprobar permisos
    error = verificar_administrador()
    if error is not None:
        return error

    mensaje = None
    codigo = 500

    try:
        eliminado = eliminar_servicio(id_servicio)

        if eliminado:
            mensaje = "Servicio dado de baja correctamente"
            codigo = 200
        else:
            mensaje = "Servicio no encontrado"
            codigo = 404

    except Error:
        mensaje = "Error al eliminar el servicio"

    return jsonify({"mensaje": mensaje}), codigo