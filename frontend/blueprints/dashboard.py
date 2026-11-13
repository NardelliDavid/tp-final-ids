import requests
from flask import Blueprint, render_template, session, redirect, url_for
from config import BACKEND_URL

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route('/admin/dashboard')
def dashboard():
    token = session.get("token")
    if not token:
        return redirect(url_for("login_admin"))
    if session.get("usuario", {}).get("rol") != "administrador":
        return redirect(url_for("login_admin"))

    # Manda la solicitud de tipo get con el token para obtener los datos del dashboard
    headers = {"Authorization": f"Bearer {token}"}
    respuesta = requests.get(
        f"{BACKEND_URL}/backoffice/dashboard",
        headers=headers,
        timeout=5
    )

    if respuesta.ok:
        resultado = respuesta.json().get("OK", [])
        datos = {
            "servicios": resultado[0],
            "totales": resultado[1],
            "generos": resultado[2],
            "peliculas": resultado[3],
        }
        return render_template('admin/dashboard.html', datos=datos)
    else:
        print(respuesta.status_code, respuesta.text)
        return render_template('admin/dashboard.html', error=respuesta.status_code)