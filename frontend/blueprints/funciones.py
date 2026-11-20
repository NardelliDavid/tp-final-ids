
import requests
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from config import BACKEND_URL

funciones_bp = Blueprint("funciones", __name__)


def obtener_headers():
    return {
        "Authorization": f"Bearer {session['token']}"
    }


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


@funciones_bp.route('/admin/funciones')
def funciones():
    if not session.get("token"):
        return redirect(url_for("auth.login_admin"))

    if session.get("usuario", {}).get("rol") != "administrador":
        return redirect(url_for("auth.login_admin"))

    funciones = []
    peliculas = []
    salas = []
    mensaje = None

    try:
        # Obtener funciones registradas
        respuesta = requests.get(
            f"{BACKEND_URL}/funciones",
            params={"incluir_pasadas": "true"},
            headers=obtener_headers(),
            timeout=5
        )

        if respuesta.ok:
            funciones = respuesta.json()
        else:
            mensaje = "No se pudieron cargar las funciones."

        # Obtener películas desde MySQL
        respuesta_peliculas = requests.get(
            f"{BACKEND_URL}/backoffice/peliculas",
            headers=obtener_headers(),
            timeout=5
        )

        if respuesta_peliculas.ok:
            peliculas = normalizar_peliculas(
                respuesta_peliculas.json()
            )

        # Obtener salas desde MySQL
        respuesta_salas = requests.get(
            f"{BACKEND_URL}/salas",
            headers=obtener_headers(),
            timeout=5
        )

        if respuesta_salas.ok:
            salas = respuesta_salas.json()

    except requests.RequestException:
        mensaje = "No se pudo conectar con el backend."

    return render_template(
        'admin/funciones.html',
        funciones=funciones,
        peliculas=peliculas,
        salas=salas,
        mensaje=mensaje
    )


@funciones_bp.route('/admin/funciones/<int:funcion_id>')
def detalle_funcion(funcion_id):
    if not session.get("token"):
        return redirect(url_for("auth.login_admin"))

    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/funciones/{funcion_id}",
            headers=obtener_headers(),
            timeout=5
        )
        return jsonify(respuesta.json()), respuesta.status_code

    except requests.RequestException:
        return jsonify({"error": "No se pudo conectar con el backend."}), 500


@funciones_bp.route('/admin/funciones/<int:funcion_id>/butacas')
def butacas_funcion(funcion_id):
    if not session.get("token"):
        return redirect(url_for("auth.login_admin"))

    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/funciones/{funcion_id}/butacas",
            headers=obtener_headers(),
            timeout=5
        )
        return jsonify(respuesta.json()), respuesta.status_code

    except requests.RequestException:
        return jsonify({"error": "No se pudo conectar con el backend."}), 500


@funciones_bp.route('/admin/funciones/crear', methods=["POST"])
def crear_funcion():
    if not session.get("token"):
        return redirect(url_for("auth.login_admin"))

    datos = request.form.to_dict()

    try:
        datos["pelicula_id"] = int(datos["pelicula_id"])
        datos["sala_id"] = int(datos["sala_id"])
        datos["precio"] = float(datos["precio"])

        respuesta = requests.post(
            f"{BACKEND_URL}/funciones",
            json=datos,
            headers=obtener_headers(),
            timeout=5
        )

        if respuesta.ok:
            return redirect(url_for("funciones.funciones"))

        return (
            f"Error al crear la función: {respuesta.status_code} - {respuesta.text}",
            respuesta.status_code
        )

    except requests.RequestException:
        return "No se pudo conectar con el backend.", 500

    except (ValueError, KeyError):
        return "Los datos ingresados no son válidos.", 400


@funciones_bp.route('/admin/funciones/<int:funcion_id>/editar', methods=["POST"])
def editar_funcion(funcion_id):
    if not session.get("token"):
        return redirect(url_for("auth.login_admin"))

    datos = request.form.to_dict()

    try:
        datos["sala_id"] = int(datos["sala_id"])
        datos["precio"] = float(datos["precio"])

        respuesta = requests.patch(
            f"{BACKEND_URL}/funciones/{funcion_id}",
            json=datos,
            headers=obtener_headers(),
            timeout=5
        )

        if respuesta.ok:
            return redirect(url_for("funciones.funciones"))

        return jsonify(respuesta.json()), respuesta.status_code

    except requests.RequestException:
        return jsonify({"error": "No se pudo conectar con el backend."}), 500

    except (ValueError, KeyError):
        return jsonify({"error": "Los datos ingresados no son válidos."}), 400


@funciones_bp.route('/admin/funciones/<int:funcion_id>/eliminar', methods=["POST"])
def eliminar_funcion(funcion_id):
    if not session.get("token"):
        return redirect(url_for("auth.login_admin"))

    try:
        respuesta = requests.delete(
            f"{BACKEND_URL}/funciones/{funcion_id}",
            headers=obtener_headers(),
            timeout=5
        )

        if respuesta.status_code == 204:
            return redirect(url_for("funciones.funciones"))

        return jsonify(respuesta.json()), respuesta.status_code

    except requests.RequestException:
        return jsonify({"error": "No se pudo conectar con el backend."}), 500
