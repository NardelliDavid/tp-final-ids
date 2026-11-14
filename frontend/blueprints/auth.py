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


# Ruta para registrar un cliente nuevo (GET muestra el formulario, POST envía los datos al backend)
@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    mensaje = None
    exito = None

    # Toma los datos que el usuario escribió si envió el formulario
    if request.method == "POST":
        datos = {
            "nombre": request.form.get("nombre", "").strip(),
            "email": request.form.get("email", "").strip(),
            "password": request.form.get("password", "")
        }

        try:
            # Envía los datos en formato JSON al endpoint de registro del backend
            respuesta = requests.post(
                f"{BACKEND_URL}/auth/registro",
                json=datos,
                timeout=5
            )

            # Muestra mensaje verde de éxito si el backend responde 201 (Creado)
            if respuesta.status_code == 201:
                exito = "Cuenta creada con éxito. Ya podés iniciar sesión."
            else:
                # Lee el mensaje de error que devuelve el backend si el email ya existe o falta algún dato
                resultado = respuesta.json()
                mensaje = resultado.get("mensaje", "No se pudo completar el registro.")

        except requests.RequestException:
            # Muestra aviso de error si el servidor backend está apagado
            mensaje = "No se pudo conectar con el backend."

    # Renderiza la pantalla HTML pasándole los mensajes de error o éxito si los hay
    return render_template("formularios/registro_user.html", mensaje=mensaje, exito=exito)


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


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
