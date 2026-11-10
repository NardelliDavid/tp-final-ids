from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__, template_folder="templates")
app.secret_key = "clave-local-desarrollo"

BACKEND_URL = "http://127.0.0.1:5000"

"Acá comienzan las rutas de las pantallas que heredan del base.html"
@app.route('/admin/dashboard')
def dashboard():
    if not session.get("token"):
        return redirect(url_for("login_admin"))
    if session.get("usuario", {}).get("rol") != "administrador":
        return redirect(url_for("login_admin"))
    return render_template('admin/dashboard.html')


@app.route('/admin/peliculas')
def peliculas():
    return render_template('admin/peliculas.html')


@app.route('/admin/funciones')
def funciones():
    return render_template('admin/funciones.html')


@app.route('/admin/horarios')
def horarios():
    return render_template('admin/horarios.html')


@app.route('/admin/ventas_estadisticas')
def ventas_estadisticas():
    return render_template('admin/ventas_estadisticas.html')


@app.route('/admin/servicios')
def servicios():
    return render_template('admin/servicios.html')


@app.route('/admin/validacion_qr')
def validacion_qr():
    return "Pantalla de validacion_qr en desarrollo"


@app.route("/")
def index():
    return redirect(url_for("login_admin"))


@app.route("/login", methods=["GET", "POST"])
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
                    return redirect(url_for("login"))

            else:
                mensaje = "No se pudo iniciar sesión. Revisá tus datos."

        except requests.RequestException:
            mensaje = "No se pudo conectar con el backend."

    return render_template("formularios/login_user.html", mensaje=mensaje)



@app.route("/login_admin", methods=["GET", "POST"])
def login_admin():
    if session.get("token"):
        return redirect(url_for("login"))
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
                    return redirect(url_for("dashboard"))

            else:
                mensaje = "No se pudo iniciar sesión. Revisá tus datos."

        except requests.RequestException:
            mensaje = "No se pudo conectar con el backend."
    return render_template("formularios/login_admin.html", mensaje=mensaje)


@app.route("/admin/formulario_validar_qr", methods=["GET", "POST"])
def formulario_validar_qr():
    if not session.get("token"):
        return redirect(url_for("login_admin"))
    if session.get("usuario", {}).get("rol") != "administrador":
        return redirect(url_for("login"))
    return render_template("formularios/validar_qr.html")
    

@app.route("/admin/qr", methods=["GET", "POST"])
def admin_qr():

    if not session.get("token"):
        return redirect(url_for("login"))

    if session.get("usuario", {}).get("rol") != "administrador":
        session.clear()
        return redirect(url_for("login"))

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
                headers={
                    "Authorization": f"Bearer {session['token']}"
                },
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
                    resultado.get(
                        "error",
                        "No se pudo validar el QR."
                    )
                )

        except requests.RequestException:
            error = "No se pudo conectar con el backend."

    return render_template(
        "admin/validar_qr.html",
        resultado=resultado,
        error=error
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(port=5001, debug=True)

