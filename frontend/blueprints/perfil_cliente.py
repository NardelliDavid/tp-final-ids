import requests
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from config import BACKEND_URL

perfil_cliente_bp = Blueprint("perfil_cliente", __name__)

 
@perfil_cliente_bp.route("/mi_perfil")
def mi_perfil():
    token = session.get("token")

    if not token:
        return redirect(url_for("auth.login"))

    usuario = {}
    compras = []
    peliculas_vistas = []
    mensaje_historial = None
    mensaje_perfil = None
    
    try:
        resp_perfil = requests.post(
            f"{BACKEND_URL}/usuarios/me",
            json={"token": token},
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
            json={"token": token},
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