import requests
from flask import Blueprint, redirect, render_template, session, url_for, request
from config import BACKEND_URL
from utils import *

perfil_cliente_bp = Blueprint("perfil_cliente", __name__)

@perfil_cliente_bp.route("/mi_perfil")
def mi_perfil():
    token = session.get("token")
    if not verificar_cliente(token):
        return redirect(url_for("auth.login"))

    headers = {"Authorization": f"Bearer {token}"}

    usuario = {}
    compras = []
    peliculas_vistas = []
    mensaje_historial = None
    mensaje_perfil = request.args.get("mensaje")
    try:
        resp_perfil = requests.get(
            f"{BACKEND_URL}/usuarios/me",
            headers=headers,
            timeout=5
        )

        if resp_perfil.status_code == 401:
            session.clear()
            return redirect(url_for("auth.login"))

        if resp_perfil.ok:
            datos_perfil = resp_perfil.json()
            if type(datos_perfil) == dict:
                usuario = datos_perfil

        else: 
            mensaje_perfil = "No se pudieron cargar los datos del usuario"

    except requests.RequestException:
        mensaje_perfil = "No se pudo conectar con el backend"

    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/usuarios/me/historial",
            headers=headers,
            timeout=5
        )

        if respuesta.status_code == 401:
            session.clear()
            return redirect(url_for("auth.login"))

        if respuesta.ok:
            historial = respuesta.json()
            compras = historial.get("compras", [])
            peliculas_vistas = historial.get("peliculas_vistas", [])
        else:
            mensaje_historial = "No se pudo cargar el historial."

    except requests.RequestException:
        mensaje_historial = "No se pudo conectar con el backend."

    return render_template(
        "cartelera/mi_perfil.html",
        usuario=usuario,
        compras=compras,
        peliculas_vistas=peliculas_vistas,
        mensaje_historial=mensaje_historial,
        mensaje_perfil=mensaje_perfil
    )

@perfil_cliente_bp.route("/perfil/modificar", methods=["POST"])
def modificar_perfil():
    token = session.get("token")
    if not verificar_cliente(token):
        return redirect(url_for("auth.login"))

    headers = {"Authorization": f"Bearer {token}"}

    payload = {}
    for campo in ("nombre", "password_actual", "password_nueva"):
        valor = request.form.get(campo, "").strip()
        if valor:
            payload[campo] = valor

    mensaje = None

    if payload:
        try:
            resp = requests.patch(
                f"{BACKEND_URL}/usuarios/me",
                json=payload,
                headers=headers,
                timeout=5
            )

            try:
                mensaje = resp.json().get("mensaje")
            except ValueError:
                mensaje = None

            # Solo cerramos sesión si el token es inválido
            if resp.status_code == 401 and mensaje == "No autorizado":
                session.clear()
                return redirect(url_for("auth.login"))

        except requests.RequestException:
            mensaje = "No se pudo conectar con el backend"

    return redirect(url_for("perfil_cliente.mi_perfil", mensaje=mensaje))