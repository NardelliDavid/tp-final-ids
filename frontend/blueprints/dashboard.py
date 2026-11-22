import requests
from datetime import date, timedelta
from flask import Blueprint, render_template, session, redirect, url_for, request
from config import BACKEND_URL

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route('/admin/dashboard')
def dashboard():

    token = session.get("token")

    if not token:
        return redirect(url_for("login_admin"))

    if session.get("usuario", {}).get("rol") != "administrador":
        return redirect(url_for("login_admin"))

    # Fechas predeterminadas: últimos 30 días.
    hoy = date.today()
    fecha_desde_default = (hoy - timedelta(days=30)).isoformat()
    fecha_hasta_default = hoy.isoformat()

    # Obtener las fechas seleccionadas por el administrador.
    desde = request.args.get("desde", fecha_desde_default)
    hasta = request.args.get("hasta", fecha_hasta_default)

    # Enviar las fechas al backend.
    headers = {
        "Authorization": f"Bearer {token}"
    }

    parametros = {
        "desde": desde,
        "hasta": hasta
    }

    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/backoffice/dashboard",
            headers=headers,
            params=parametros,
            timeout=10
        )

        if respuesta.ok:
            resultado = respuesta.json().get("OK", {})

            return render_template(
                'admin/dashboard.html',
                datos=resultado,
                desde=desde,
                hasta=hasta
            )

        else:
            print(respuesta.status_code, respuesta.text)

            return render_template(
                'admin/dashboard.html',
                error=respuesta.json().get("Error", respuesta.status_code),
                desde=desde,
                hasta=hasta
            )

    except requests.exceptions.RequestException as e:
        print("Error al conectar con el backend:", e)

        return render_template(
            'admin/dashboard.html',
            error="No se pudo conectar con el servidor.",
            desde=desde,
            hasta=hasta
        )
