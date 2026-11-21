import requests
from flask import (Blueprint, render_template, request, session,
                   redirect, url_for)
from config import BACKEND_URL

qr_bp = Blueprint("qr", __name__)


@qr_bp.route('/admin/validacion_qr')
def validacion_qr():
    if not session.get("token"):
        return redirect(url_for("auth.login_admin"))
    if session.get("usuario", {}).get("rol") != "administrador":
        return redirect(url_for("auth.login_admin"))
    return "Pantalla de validacion_qr en desarrollo"


@qr_bp.route("/admin/formulario_validar_qr", methods=["GET", "POST"])
def formulario_validar_qr():
    if not session.get("token"):
        return redirect(url_for("auth.login_admin"))
    if session.get("usuario", {}).get("rol") != "administrador":
        return redirect(url_for("auth.login"))
    return render_template("formularios/validar_qr.html")


@qr_bp.route("/admin/qr", methods=["GET", "POST"])
def admin_qr():
    if not session.get("token"):
        return redirect(url_for("auth.login"))

    if session.get("usuario", {}).get("rol") != "administrador":
        session.clear()
        return redirect(url_for("auth.login"))

    resultado = None
    error = None

    if request.method == "POST":
        try:
            funcion_id = int(request.form.get("funcion_id", ""))
        except ValueError:
            funcion_id = 0

        datos = {
            "token": request.form.get("qr_token", "").strip(),
            "funcion_id": funcion_id,
        }

        try:
            respuesta = requests.post(
                f"{BACKEND_URL}/qr/validaciones",
                json=datos,
                headers={"Authorization": f"Bearer {session['token']}"},
                timeout=5
            )

            try:
                resultado = respuesta.json()
            except ValueError:
                resultado = {
                    "mensaje": "El backend devolvió una respuesta no válida."
                }

            if not respuesta.ok:
                error = resultado.get(
                    "mensaje",
                    resultado.get("error", "No se pudo validar el QR.")
                )

        except requests.RequestException:
            error = "No se pudo conectar con el backend."

    return render_template(
        "admin/validar_qr.html",
        resultado=resultado,
        error=error
    )