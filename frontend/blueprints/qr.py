import requests
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for
)
from utils import *
from config import BACKEND_URL

qr_bp = Blueprint("qr", __name__)


@qr_bp.route('/admin/validacion_qr')
def validacion_qr():
    if not verificar_administrador(session.get("token")):
        return redirect(url_for("auth.login_admin"))

    return redirect(url_for("qr.admin_qr"))


@qr_bp.route("/admin/formulario_validar_qr", methods=["GET", "POST"])
def formulario_validar_qr():
    if not verificar_administrador(session.get("token")):
        return redirect(url_for("auth.login_admin"))

    return render_template("admin/validar_qr.html")


@qr_bp.route("/admin/qr", methods=["GET", "POST"])
def admin_qr():
    if not verificar_administrador(session.get("token")):
        return redirect(url_for("auth.login_admin"))

    resultado = None
    error = None

    if request.method == "POST":

        try:
            funcion_id = int(request.form.get("funcion_id", ""))
        except (ValueError, TypeError):
            funcion_id = 0

        datos = {
            "token": request.form.get("qr_token", "").strip(),
            "funcion_id": funcion_id,
        }

        if not datos["token"]:
            error = "Ingresá el token del QR."

        elif funcion_id <= 0:
            error = "Ingresá un número de función válido."

        else:
            try:
                respuesta = requests.post(
                    f"{BACKEND_URL}/qr/validaciones",
                    json=datos,
                    headers={
                        "Authorization": f"Bearer {session['token']}"
                    },
                    timeout=5
                )

                try:
                    resultado = respuesta.json()
                except ValueError:
                    resultado = {}

                if not respuesta.ok:
                    error = resultado.get(
                        "mensaje",
                        resultado.get(
                            "error",
                            "No se pudo validar el QR."
                        )
                    )
                    resultado = None

                elif not resultado.get("valido"):
                    error = resultado.get(
                        "mensaje",
                        "No se pudo validar el QR."
                    )
                    resultado = None

            except requests.RequestException:
                error = "No se pudo conectar con el backend."

    return render_template(
        "admin/validar_qr.html",
        resultado=resultado,
        error=error
    )
