from flask import Flask, render_template, request, redirect, url_for, session
import requests
import math

app = Flask(__name__)
app.secret_key = "clave-local-desarrollo"

BACKEND_URL = "http://127.0.0.1:5000"


# ========================================
# PANTALLAS DEL BACKOFFICE
# ========================================

@app.route('/admin/dashboard')
def dashboard():
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


# ========================================
# SERVICIOS ADICIONALES
# ========================================

# Mostrar los servicios existentes

@app.route('/admin/servicios')
def servicios():

    if not session.get("token"):
        return redirect(url_for("login"))

    if session.get("usuario", {}).get("rol") != "administrador":
        session.clear()
        return redirect(url_for("login"))

    lista_servicios = []
    error = None

    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/servicios",
            timeout=5
        )

        if respuesta.ok:
            lista_servicios = respuesta.json()
        else:
            error = "No se pudieron obtener los servicios."

    except (requests.RequestException, ValueError):
        error = "No se pudo obtener una respuesta válida del backend."

    return render_template(
        'admin/servicios.html',
        servicios=lista_servicios,
        error=error
    )


# Crear un nuevo servicio

@app.route('/admin/servicios/nuevo', methods=['POST'])
def crear_servicio():

    if not session.get("token"):
        return redirect(url_for("login"))

    if session.get("usuario", {}).get("rol") != "administrador":
        session.clear()
        return redirect(url_for("login"))

    nombre = request.form.get('nombre', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    precio = request.form.get('precio', '')

    if not nombre or not precio:
        return "El nombre y el precio son obligatorios.", 400

    try:
        precio = float(precio)

        if not math.isfinite(precio) or precio <= 0:
            return "El precio debe ser un número válido mayor a cero.", 400

    except ValueError:
        return "El precio ingresado no es válido.", 400

    nuevo_servicio = {
        'nombre': nombre,
        'descripcion': descripcion,
        'precio': precio
    }

    try:
        respuesta = requests.post(
            f"{BACKEND_URL}/servicios",
            json=nuevo_servicio,
            headers={
                "Authorization": f"Bearer {session['token']}"
            },
            timeout=5
        )

        if respuesta.status_code != 201:
            return "No se pudo crear el servicio.", 502

    except requests.RequestException:
        return "No se pudo conectar con el backend.", 502

    return redirect(url_for('servicios'))


# Editar un servicio

@app.route('/admin/servicios/editar/<int:id_servicio>', methods=['POST'])
def editar_servicio_frontend(id_servicio):

    if not session.get("token"):
        return redirect(url_for("login"))

    if session.get("usuario", {}).get("rol") != "administrador":
        session.clear()
        return redirect(url_for("login"))

    nombre = request.form.get('nombre', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    precio = request.form.get('precio', '')

    if not nombre or not precio:
        return "El nombre y el precio son obligatorios.", 400

    try:
        precio = float(precio)

        if not math.isfinite(precio) or precio <= 0:
            return "El precio debe ser un número válido mayor a cero.", 400

    except ValueError:
        return "El precio ingresado no es válido.", 400

    datos = {
        'nombre': nombre,
        'descripcion': descripcion,
        'precio': precio
    }

    try:
        respuesta = requests.patch(
            f"{BACKEND_URL}/servicios/{id_servicio}",
            json=datos,
            headers={
                "Authorization": f"Bearer {session['token']}"
            },
            timeout=5
        )

        if not respuesta.ok:
            return "No se pudo modificar el servicio.", 502

    except requests.RequestException:
        return "No se pudo conectar con el backend.", 502

    return redirect(url_for('servicios'))


# Eliminar un servicio

@app.route('/admin/servicios/eliminar/<int:id_servicio>', methods=['POST'])
def eliminar_servicio_frontend(id_servicio):

    if not session.get("token"):
        return redirect(url_for("login"))

    if session.get("usuario", {}).get("rol") != "administrador":
        session.clear()
        return redirect(url_for("login"))

    try:
        respuesta = requests.delete(
            f"{BACKEND_URL}/servicios/{id_servicio}",
            headers={
                "Authorization": f"Bearer {session['token']}"
            },
            timeout=5
        )

        if not respuesta.ok:
            return "No se pudo eliminar el servicio.", 502

    except requests.RequestException:
        return "No se pudo conectar con el backend.", 502

    return redirect(url_for('servicios'))


# ========================================
# VALIDACIÓN QR
# ========================================

@app.route('/admin/validacion_qr')
def validacion_qr():
    return "Pantalla de validacion_qr en desarrollo"


# ========================================
# INICIO Y LOGIN
# ========================================

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

    return render_template(
        "admin/login.html",
        mensaje=mensaje
    )


# ========================================
# ADMINISTRACIÓN DE QR
# ========================================

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


# ========================================
# CERRAR SESIÓN
# ========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ========================================
# EJECUTAR FRONTEND
# ========================================

if __name__ == "__main__":
    app.run(port=5001, debug=True)