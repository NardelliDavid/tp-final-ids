from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__, template_folder="templates")
app.secret_key = "clave-local-desarrollo"

BACKEND_URL = "http://127.0.0.1:5000"

@app.route('/admin/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

@app.route("/")
def index():
    return redirect(url_for("login"))


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

                if usuario.get("rol") != "administrador":
                    mensaje = "Acceso restringido a administradores."
                else:
                    session["token"] = resultado["token"]
                    session["usuario"] = usuario
                    return redirect(url_for("admin_qr"))

            else:
                mensaje = "No se pudo iniciar sesión. Revisá tus datos."

        except requests.RequestException:
            mensaje = "No se pudo conectar con el backend."

    return render_template("index.html", mensaje=mensaje)


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
        datos = {
            "codigo_qr": request.form.get("qr_token", "").strip(),
        }

        try:

            respuesta = requests.post(
                f"{BACKEND_URL}/qr/validar",
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
        "index.html",
        resultado=resultado,
        error=error
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(port=5001, debug=True)