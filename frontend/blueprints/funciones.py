
import requests
from flask import Blueprint, render_template, session, redirect, url_for, request
from config import BACKEND_URL
from utils import *

funciones_bp = Blueprint("funciones", __name__)

def normalizar_peliculas(datos):
    """
    Adapta la respuesta del backend para obtener
    una lista de películas con id y titulo.
    """

    if isinstance(datos, dict):
        datos = datos.get("OK", datos.get("peliculas", []))

    elif (
        isinstance(datos, list)
        and len(datos) > 0
        and isinstance(datos[0], dict)
        and "OK" in datos[0]
    ):
        datos = datos[0]["OK"]

    peliculas = []

    for pelicula in datos:
        if isinstance(pelicula, dict):
            peliculas.append({
                "id": pelicula.get("id"),
                "titulo": pelicula.get("titulo")
            })

        elif isinstance(pelicula, (list, tuple)) and len(pelicula) >= 3:
            peliculas.append({
                "id": pelicula[0],
                "titulo": pelicula[2]
            })

    return [
        pelicula for pelicula in peliculas
        if pelicula["id"] is not None and pelicula["titulo"]
    ]


def obtener_mensaje_error(respuesta, accion):
    try:
        datos = respuesta.json()
    except ValueError:
        datos = None

    error = datos

    if isinstance(error, dict):
        error = (
            error.get("error")
            or error.get("mensaje")
            or error.get("message")
        )

    while isinstance(error, dict):
        error = (
            error.get("error")
            or error.get("mensaje")
            or error.get("message")
        )

    if not isinstance(error, str) or not error.strip():
        return (
            f"No se pudo {accion}. "
            "Revisá los datos e intentá nuevamente."
        )

    error_minusculas = error.lower()

    if "no puede programarse en el pasado" in error_minusculas:
        return (
            "La fecha y hora deben ser posteriores al momento actual. "
            "Revisá los datos e intentá nuevamente."
        )

    if "la sala no existe" in error_minusculas:
        return "La sala seleccionada no existe. Elegí otra sala."

    if "la película no existe" in error_minusculas:
        return "La película seleccionada no existe."

    if "formato de fecha" in error_minusculas:
        return "El formato de la fecha y hora no es válido."

    if "faltan datos obligatorios" in error_minusculas:
        return "Completá todos los campos obligatorios."

    if "datos enviados no son válidos" in error_minusculas:
        return (
            "Los datos ingresados no son válidos. "
            "Revisalos e intentá nuevamente."
        )

    if "horario" in error_minusculas or "superposicion" in error_minusculas:
        return (
            "La sala ya tiene otra función en ese horario "
            "o no cumple el tiempo de limpieza."
        )

    return error


def redirigir_funciones(mensaje, tipo="error"):
    return redirect(url_for(
        "funciones.funciones",
        mensaje=mensaje,
        tipo_mensaje=tipo
    ))


@funciones_bp.route('/admin/funciones')
def funciones():
    token = session.get("token")
    if not verificar_administrador(token):
        return redirect(url_for("auth.login_admin"))

    lista_funciones = []
    peliculas = []
    salas = []

    mensaje = request.args.get("mensaje")
    tipo_mensaje = request.args.get("tipo_mensaje", "error")

    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/funciones",
            params={"incluir_pasadas": "true"},
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )

        if respuesta.ok:
            lista_funciones = respuesta.json()
        elif not mensaje:
            mensaje = "No se pudieron cargar las funciones."
            tipo_mensaje = "error"

        respuesta_peliculas = requests.get(
            f"{BACKEND_URL}/backoffice/peliculas",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )

        if respuesta_peliculas.ok:
            peliculas = normalizar_peliculas(
                respuesta_peliculas.json()
            )

        respuesta_salas = requests.get(
            f"{BACKEND_URL}/salas",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )

        if respuesta_salas.ok:
            salas = respuesta_salas.json()

    except requests.RequestException:
        mensaje = "No se pudo conectar con el backend."
        tipo_mensaje = "error"

    return render_template(
        'admin/funciones.html',
        funciones=lista_funciones,
        peliculas=peliculas,
        salas=salas,
        mensaje=mensaje,
        tipo_mensaje=tipo_mensaje
    )


@funciones_bp.route('/admin/funciones/<int:funcion_id>')
def detalle_funcion(funcion_id):
    token = session.get("token")
    if not verificar_administrador(token):
        return redirect(url_for("auth.login_admin"))

    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/funciones/{funcion_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )

        if not respuesta.ok:
            return redirigir_funciones(
                obtener_mensaje_error(respuesta, "obtener el detalle")
            )

        datos = respuesta.json()

        if isinstance(datos, dict) and "OK" in datos:
            datos = datos["OK"]

        if not isinstance(datos, dict):
            return redirigir_funciones(
                "La información de la función no tiene un formato válido."
            )

        return render_template(
            'admin/detalle_funcion.html',
            funcion=datos
        )

    except requests.RequestException:
        return redirigir_funciones(
            "No se pudo conectar con el backend."
        )

    except ValueError:
        return redirigir_funciones(
            "No se pudo interpretar la información de la función."
        )


@funciones_bp.route('/admin/funciones/<int:funcion_id>/butacas')
def butacas_funcion(funcion_id):
    token = session.get("token")
    if not verificar_administrador(token):
        return redirect(url_for("auth.login_admin"))

    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/funciones/{funcion_id}/butacas",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )

        if not respuesta.ok:
            return redirigir_funciones(
                obtener_mensaje_error(respuesta, "obtener las butacas")
            )

        datos = respuesta.json()

        if isinstance(datos, dict) and "OK" in datos:
            datos = datos["OK"]

        if not isinstance(datos, dict):
            return redirigir_funciones(
                "La información de las butacas no tiene un formato válido."
            )

        lista_butacas = datos.get("butacas", [])

        if not isinstance(lista_butacas, list):
            lista_butacas = []

        libres = 0
        ocupadas = 0

        for butaca in lista_butacas:
            estado = str(butaca.get("estado", "")).lower()

            if estado == "libre":
                libres += 1
                butaca["estado_css"] = "libre"
            else:
                ocupadas += 1
                butaca["estado_css"] = "ocupada"

        return render_template(
            'admin/butacas_funcion.html',
            funcion_id=funcion_id,
            butacas=lista_butacas,
            filas=datos.get("filas", 0),
            columnas=datos.get("columnas", 0),
            libres=libres,
            ocupadas=ocupadas
        )

    except requests.RequestException:
        return redirigir_funciones(
            "No se pudo conectar con el backend."
        )

    except ValueError:
        return redirigir_funciones(
            "No se pudo interpretar la información de las butacas."
        )


@funciones_bp.route('/admin/funciones/crear', methods=["POST"])
def crear_funcion():
    token = session.get("token")
    if not verificar_administrador(token):
        return redirect(url_for("auth.login_admin"))

    datos = request.form.to_dict()

    try:
        datos["pelicula_id"] = int(datos["pelicula_id"])
        datos["sala_id"] = int(datos["sala_id"])
        datos["precio"] = float(datos["precio"])

        respuesta = requests.post(
            f"{BACKEND_URL}/funciones",
            json=datos,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )

        if respuesta.ok:
            return redirigir_funciones(
                "La función se creó correctamente.",
                "exito"
            )

        return redirigir_funciones(
            obtener_mensaje_error(respuesta, "crear la función")
        )

    except requests.RequestException:
        return redirigir_funciones(
            "No se pudo conectar con el backend."
        )

    except (ValueError, KeyError):
        return redirigir_funciones(
            "Los datos ingresados no son válidos. Revisalos e intentá nuevamente."
        )


@funciones_bp.route('/admin/funciones/<int:funcion_id>/editar', methods=["POST"])
def editar_funcion(funcion_id):
    token = session.get("token")
    if not verificar_administrador(token):
        return redirect(url_for("auth.login_admin"))

    datos = request.form.to_dict()

    try:
        datos["sala_id"] = int(datos["sala_id"])
        datos["precio"] = float(datos["precio"])

        respuesta = requests.patch(
            f"{BACKEND_URL}/funciones/{funcion_id}",
            json=datos,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )

        if respuesta.ok:
            return redirigir_funciones(
                "Los cambios de la función se guardaron correctamente.",
                "exito"
            )

        return redirigir_funciones(
            obtener_mensaje_error(respuesta, "modificar la función")
        )

    except requests.RequestException:
        return redirigir_funciones(
            "No se pudo conectar con el backend."
        )

    except (ValueError, KeyError):
        return redirigir_funciones(
            "Los datos ingresados no son válidos. Revisalos e intentá nuevamente."
        )


@funciones_bp.route('/admin/funciones/<int:funcion_id>/eliminar', methods=["POST"])
def eliminar_funcion(funcion_id):
    token = session.get("token")
    if not verificar_administrador(token):
        return redirect(url_for("auth.login_admin"))

    try:
        respuesta = requests.delete(
            f"{BACKEND_URL}/funciones/{funcion_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )

        if respuesta.status_code == 204:
            return redirigir_funciones(
                "La función se eliminó correctamente.",
                "exito"
            )

        return redirigir_funciones(
            obtener_mensaje_error(respuesta, "eliminar la función")
        )

    except requests.RequestException:
        return redirigir_funciones(
            "No se pudo conectar con el backend."
        )
