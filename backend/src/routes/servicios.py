from flask import Blueprint, jsonify, request
from mysql.connector import Error
from src.repositories.servicios_repository import obtener_servicios_activos, crear_servicio,modificar_servicio,eliminar_servicio

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
    

#se encarga de gestionar la creación de un nuevo servicio en Cine
@servicios_bp.route("/servicios", methods=["POST"])
def agregar_servicio():

    datos = request.get_json(silent=True) #si el JSON está mal formado o no se puede interpretar como JSON, el método devuelva None en lugar de generar un error HTTP automáticamente.

    if type(datos) != dict:
        return jsonify({"mensaje": "JSON inválido"}), 400

    nombre = datos.get("nombre")
    descripcion = datos.get("descripcion")
    precio = datos.get("precio")

    # Validamos que estén los datos obligatorios
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
        return jsonify({ "mensaje": "Servicio creado correctamente", "id": id_servicio}), 201
    
    except Error:
        return jsonify({"mensaje": "Error al crear el servicio"}), 500


@servicios_bp.route("/servicios/<int:id_servicio>", methods=["PATCH"])
def modificar_servicio_endpoint(id_servicio):

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



@servicios_bp.route("/servicios/<int:id_servicio>", methods=["DELETE"])
def eliminar_servicio_endpoint(id_servicio):

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

