import requests
from flask import Blueprint, render_template, request, session, redirect, url_for
from utils import *
from config import BACKEND_URL

servicios_bp = Blueprint("servicios", __name__)


@servicios_bp.route("/admin/servicios")
def servicios():
    if not verificar_administrador(session.get("token")):
        return redirect(url_for("auth.login_admin"))

    respuesta = requests.get(f"{BACKEND_URL}/servicios", timeout=5)
    lista_servicios = respuesta.json()
    return render_template("admin/servicios.html", servicios=lista_servicios)


@servicios_bp.route("/admin/servicios/nuevo", methods=["POST"])
def nuevo_servicio():
    token = session.get("token")
    if not verificar_administrador(token):
        return redirect(url_for("auth.login_admin"))

    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    precio = request.form.get("precio", type=float)

    if not nombre or precio is None or precio <= 0:
        return "Ingresá un nombre y un precio mayor a cero.", 400

    datos = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
    }

    try:
        respuesta = requests.post(
            f"{BACKEND_URL}/servicios",
            json=datos,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
    except requests.RequestException:
        return "No se pudo conectar con el backend.", 502

    if respuesta.status_code != 201:
        return "El backend no pudo crear el servicio.", respuesta.status_code

    return redirect(url_for("servicios.servicios"))

@servicios_bp.route("/admin/servicios/<int:id_servicio>/eliminar", methods=["POST"])
def eliminar_servicio(id_servicio):
    token = session.get("token")
    if not verificar_administrador(token):
        return redirect(url_for("auth.login_admin"))

    try:
        respuesta = requests.delete(
            f"{BACKEND_URL}/servicios/{id_servicio}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
    except requests.RequestException:
        return "No se pudo conectar con el backend.", 502

    if respuesta.status_code != 200:
        return "El backend no pudo dar de baja el servicio.", respuesta.status_code

    return redirect(url_for("servicios.servicios"))

@servicios_bp.route("/admin/servicios/<int:id_servicio>/editar", methods=["POST"])
def editar_servicio(id_servicio):
    token = session.get("token")
    if not verificar_administrador(token):
        return redirect(url_for("auth.login_admin"))

    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    precio = request.form.get("precio", type=float)

    if not nombre or precio is None or precio <= 0:
        return "Ingresá un nombre y un precio mayor a cero.", 400

    datos = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
    }

    try:
        respuesta = requests.patch(
            f"{BACKEND_URL}/servicios/{id_servicio}",
            json=datos,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
    except requests.RequestException:
        return "No se pudo conectar con el backend.", 502

    if respuesta.status_code != 200:
        return "El backend no pudo editar el servicio.", respuesta.status_code

    return redirect(url_for("servicios.servicios"))
    