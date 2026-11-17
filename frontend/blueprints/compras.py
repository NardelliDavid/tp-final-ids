import requests
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from config import BACKEND_URL

compras_bp = Blueprint("compras", __name__)


@compras_bp.route("/compras/nueva/<int:funcion_id>")
def nueva_compra(funcion_id):
    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/funciones/{funcion_id}/butacas",
            timeout=5,
        )
        respuesta_servicios = requests.get(f"{BACKEND_URL}/servicios", timeout=5)        
    except requests.RequestException:
        return "No se pudo conectar con el backend.", 502

    if respuesta.status_code != 200:
        return "No se pudieron cargar las butacas.", respuesta.status_code

    grilla = respuesta.json()
    if respuesta_servicios.status_code != 200:
        return "No se pudieron cargar los servicios.", respuesta_servicios.status_code

    return render_template(
        "compras/butacas.html",
        grilla=grilla,
        servicios=respuesta_servicios.json(),
    )
    
@compras_bp.route("/compras/nueva/<int:funcion_id>", methods=["POST"])
def confirmar_compra(funcion_id):
    destino = url_for("compras.nueva_compra", funcion_id=funcion_id)
    token = session.get("token")
    usuario = session.get("usuario", {})

    if not token or usuario.get("rol") != "cliente":
        flash("Iniciá sesión con una cuenta de cliente para comprar.")
        return redirect(destino)

    butacas = request.form.getlist("butacas")
    servicios = []

    try:
        for campo, valor in request.form.items():
            if campo.startswith("servicio_") and valor:
                cantidad = int(valor)
                if cantidad != 0:
                    servicio_id = int(campo.removeprefix("servicio_"))
                    servicios.append({
                        "servicio_id": servicio_id,
                        "cantidad": cantidad,
                    })
    except ValueError:
        flash("Revisá las cantidades de los servicios.")
        return redirect(destino)

    datos = {
        "funcion_id": funcion_id,
        "butacas": butacas,
        "servicios": servicios,
    }

    try:
        respuesta = requests.post(
            f"{BACKEND_URL}/compras",
            json=datos,
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
        resultado = respuesta.json()
    except requests.RequestException:
        flash("No se pudo obtener una respuesta del backend.")
        return redirect(destino)

    if respuesta.status_code == 201:
        return redirect(
            url_for("compras.detalle_compra", id_compra=resultado["id"])
        )

    flash(resultado.get("mensaje", "No se pudo confirmar la compra."))
    return redirect(destino)

@compras_bp.route("/compras/<int:id_compra>")
def detalle_compra(id_compra):
    token = session.get("token")

    if not token:
        return redirect(url_for("auth.login"))

    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/compras/{id_compra}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
    except requests.RequestException:
        return "No se pudo conectar con el backend.", 502

    if respuesta.status_code != 200:
        return "No se pudo consultar esta compra.", respuesta.status_code

    return render_template(
        "compras/detalle.html",
        compra=respuesta.json(),
    )
    
@compras_bp.route("/compras/<int:id_compra>/cancelar", methods=["POST"])
def cancelar_compra(id_compra):
    token = session.get("token")

    if not token:
        return redirect(url_for("auth.login"))

    try:
        respuesta = requests.post(
            f"{BACKEND_URL}/compras/{id_compra}/cancelacion",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
        resultado = respuesta.json()
    except requests.RequestException:
        flash("No se pudo obtener una respuesta del backend.")
        return redirect(
            url_for("compras.detalle_compra", id_compra=id_compra)
        )

    flash(resultado.get("mensaje", "No se pudo procesar la cancelación."))

    return redirect(
        url_for("compras.detalle_compra", id_compra=id_compra)
    )