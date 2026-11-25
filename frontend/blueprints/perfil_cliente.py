import requests
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from config import BACKEND_URL

perfil_cliente_bp = Blueprint("perfil_cliente", __name__)

def obtener_datos_perfil(token):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.get(f"{BACKEND_URL}/usuarios/me", headers=headers, timeout=5)
    if resp.status_code == 200:
        return resp.json(), None
    datos = resp.json() if resp.content else {}
    return {}, datos.get("mensaje", "No se pudieron cargar los datos del perfil.")

def obtener_historial(token):
    headers = {"Authorization": f"Bearer {token}"}
    respuesta = requests.get(
        f"{BACKEND_URL}/usuarios/me/historial",
        headers=headers,
        timeout=5,
    )
    if respuesta.status_code == 401:
        return [], [], None, True
    if respuesta.ok:
        historial = respuesta.json() if respuesta.content else {}
        compras = historial.get("compras", [])
        peliculas_vistas = historial.get("peliculas_vistas", [])
        return compras, peliculas_vistas, None, False
    return [], [], "No se pudo cargar el historial.", False

@perfil_cliente_bp.route("/mi_perfil", methods=["GET", "POST"])
def mi_perfil():
    token = session.get("token")

    if not token:
        return redirect(url_for("auth.login"))

    mensaje_error = None
    mensaje_exito = None

    if request.method == "POST":
        nombre_nuevo = request.form.get("nombre", "").strip()
        pwd_actual = request.form.get("password_actual", "")
        pwd_nueva = request.form.get("password_nueva", "")

        payload = {"nombre": nombre_nuevo}
        if pwd_actual:
            payload["password_actual"] = pwd_actual
        if pwd_nueva:
            payload["password_nueva"] = pwd_nueva

        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.patch(
            f"{BACKEND_URL}/usuarios/me",
            json=payload,
            headers=headers,
            timeout=5,
        )
        datos_resp = resp.json() if resp.content else {}

        if resp.status_code == 401:
            session.clear()
            return redirect(url_for("auth.login"))
        elif resp.status_code == 200:
            mensaje_exito = datos_resp.get("mensaje", "Datos actualizados correctamente.")
        else:
            mensaje_error = datos_resp.get("mensaje", "No se pudieron actualizar los datos.")

    usuario, error_carga = obtener_datos_perfil(token)
    if error_carga and not mensaje_error:
        mensaje_error = error_carga

    compras, peliculas_vistas, mensaje_historial, no_autorizado = obtener_historial(token)
    if no_autorizado:
        session.clear()
        return redirect(url_for("auth.login"))

    return render_template(
        "cartelera/mi_perfil.html",
        usuario=usuario,
        mensaje_error=mensaje_error,
        mensaje_exito=mensaje_exito,
        compras=compras,
        peliculas_vistas=peliculas_vistas,
        mensaje_historial=mensaje_historial,
    )