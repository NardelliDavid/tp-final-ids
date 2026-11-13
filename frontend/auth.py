import requests
from flask import (Blueprint, render_template, request, session,
                   redirect, url_for)
from config import BACKEND_URL

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    mensaje = None

    if request.method == "POST":
        datos = {
            "email": request.form.get("email", "").strip(),
            "password": request.form.get("password", "")
        }

        try:
            respuesta = requests.post(
                f"{BACKEND_URL}/auth/login",
                json=datos,
                timeout=5
            )

            if respuesta.ok:
                resultado = respuesta.json()
                usuario = resultado.get("usuario", {})

                if usuario.get("rol") != "cliente":
                    mensaje = "Acceso restringido a clientes."
                else:
                    session["token"] = resultado["token"]
                    session["usuario"] = usuario
                    return redirect(url_for("auth.login"))

            else:
                mensaje = "No se pudo iniciar sesión. Revisá tus datos."

        except requests.RequestException:
            mensaje = "No se pudo conectar con el backend."

    return render_template("formularios/login_user.html", mensaje=mensaje)


@auth_bp.route("/login_admin", methods=["GET", "POST"])
def login_admin():
    if session.get("token"):
        return redirect(url_for("auth.login"))
    mensaje = None

    if request.method == "POST":
        datos = {
            "email": request.form.get("email", "").strip(),
            "password": request.form.get("password", "")
        }

        try:
            respuesta = requests.post(
                f"{BACKEND_URL}/auth/login",
                json=datos,
                timeout=5
            )

            if respuesta.ok:
                resultado = respuesta.json()
                usuario = resultado.get("usuario", {})

                if usuario.get("rol") != "administrador":
                    mensaje = "Acceso restringido a administradores."
                else:
                    session["token"] = resultado["token"]
                    session["usuario"] = usuario
                    session["rol"] = usuario.get("rol")
                    return redirect(url_for("dashboard.dashboard"))

            else:
                mensaje = "No se pudo iniciar sesión. Revisá tus datos."

        except requests.RequestException:
            mensaje = "No se pudo conectar con el backend."

    return render_template("formularios/login_admin.html", mensaje=mensaje)