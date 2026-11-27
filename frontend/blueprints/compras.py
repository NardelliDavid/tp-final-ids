import base64
import io
import requests
import qrcode

from datetime import datetime, timedelta

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from config import BACKEND_URL
from utils import *

compras_bp = Blueprint("compras", __name__)

CLAVE_COMPRA_PENDIENTE = "compra_pendiente"


@compras_bp.route("/compras/nueva/<int:funcion_id>")
def nueva_compra(funcion_id):
    token = session.get("token")
    if not verificar_cliente(token):
        return redirect(url_for("auth.login"))
    
    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/funciones/{funcion_id}/butacas",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )

        respuesta_servicios = requests.get(
            f"{BACKEND_URL}/servicios",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )

    except requests.RequestException:
        return "No se pudo conectar con el backend.", 502

    if respuesta.status_code != 200:
        return "No se pudieron cargar las butacas.", respuesta.status_code

    if respuesta_servicios.status_code != 200:
        return "No se pudieron cargar los servicios.", respuesta_servicios.status_code

    compra_pendiente = session.get(CLAVE_COMPRA_PENDIENTE, {})

    if compra_pendiente.get("funcion_id") != funcion_id:
        compra_pendiente = {}

    return render_template(
        "compras/butacas.html",
        grilla=respuesta.json(),
        servicios=respuesta_servicios.json(),
        butacas_seleccionadas=compra_pendiente.get("butacas", []),
        cantidades_servicios=compra_pendiente.get("cantidades_servicios", {}),
    )


# Recibe la selección y la guarda temporalmente.
# Todavía NO registra la compra.
@compras_bp.route(
    "/compras/nueva/<int:funcion_id>",
    methods=["POST"],
)
def confirmar_compra(funcion_id):
    token = session.get("token")
    if not verificar_cliente(token):
        return redirect(url_for("auth.login"))
    
    destino = url_for("compras.nueva_compra", funcion_id=funcion_id)

    butacas = request.form.getlist("butacas")

    if not butacas:
        flash("Seleccioná al menos una butaca.")
        return redirect(destino)

    cantidades_servicios = {}

    try:
        for campo, valor in request.form.items():
            if campo.startswith("servicio_"):
                servicio_id = campo.removeprefix("servicio_")
                cantidad = int(valor)

                if not servicio_id.isdigit() or cantidad < 0:
                    raise ValueError

                if cantidad > 0:
                    cantidades_servicios[servicio_id] = cantidad

    except ValueError:
        flash("Revisá las cantidades de los servicios.")
        return redirect(destino)

    session[CLAVE_COMPRA_PENDIENTE] = {
        "funcion_id": funcion_id,
        "butacas": butacas,
        "cantidades_servicios": cantidades_servicios,
    }

    return redirect(
        url_for("compras.revisar_compra", funcion_id=funcion_id)
    )


# Muestra el resumen antes de registrar la compra.
@compras_bp.route("/compras/nueva/<int:funcion_id>/revision")
def revisar_compra(funcion_id):
    token = session.get("token")

    compra_pendiente = session.get(CLAVE_COMPRA_PENDIENTE)

    if not compra_pendiente or compra_pendiente.get("funcion_id") != funcion_id:
        flash("Primero tenés que seleccionar tus butacas.")
        return redirect(
            url_for("compras.nueva_compra", funcion_id=funcion_id)
        )

    try:
        respuesta_funcion = requests.get(
            f"{BACKEND_URL}/funciones/{funcion_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )

        respuesta_servicios = requests.get(
            f"{BACKEND_URL}/servicios",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )

    except requests.RequestException:
        return "No se pudo conectar con el backend.", 502

    if respuesta_funcion.status_code != 200:
        return "No se pudo cargar la información de la función.", respuesta_funcion.status_code

    if respuesta_servicios.status_code != 200:
        return "No se pudieron cargar los servicios.", respuesta_servicios.status_code

    funcion = respuesta_funcion.json()
    servicios_disponibles = respuesta_servicios.json()

    precio_entrada = float(funcion["precio"])
    butacas = compra_pendiente["butacas"]

    total_entradas = precio_entrada * len(butacas)
    servicios_seleccionados = []
    total_servicios = 0

    cantidades = compra_pendiente.get("cantidades_servicios", {})

    for servicio in servicios_disponibles:
        cantidad = int(cantidades.get(str(servicio["id"]), 0))

        if cantidad > 0:
            precio = float(servicio["precio"])
            subtotal = precio * cantidad

            servicios_seleccionados.append({
                "id": servicio["id"],
                "nombre": servicio["nombre"],
                "cantidad": cantidad,
                "precio": precio,
                "subtotal": subtotal,
            })

            total_servicios += subtotal

    total = total_entradas + total_servicios

    return render_template(
        "compras/checkout.html",
        funcion=funcion,
        butacas=butacas,
        precio_entrada=precio_entrada,
        total_entradas=total_entradas,
        servicios=servicios_seleccionados,
        total_servicios=total_servicios,
        total=total,
    )


# Registra la compra solamente después de la confirmación final.
@compras_bp.route(
    "/compras/nueva/<int:funcion_id>/confirmar",
    methods=["POST"],
)
def finalizar_compra(funcion_id):
    token = session.get("token")
    
    destino = url_for("compras.revisar_compra", funcion_id=funcion_id)

    compra_pendiente = session.get(CLAVE_COMPRA_PENDIENTE)

    if not compra_pendiente or compra_pendiente.get("funcion_id") != funcion_id:
        flash("No encontramos una selección para confirmar.")
        return redirect(
            url_for("compras.nueva_compra", funcion_id=funcion_id)
        )

    servicios = []

    for servicio_id, cantidad in compra_pendiente.get(
        "cantidades_servicios", {}
    ).items():
        servicios.append({
            "servicio_id": int(servicio_id),
            "cantidad": int(cantidad),
        })

    datos = {
        "funcion_id": funcion_id,
        "butacas": compra_pendiente["butacas"],
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

    except (requests.RequestException, ValueError):
        flash("No se pudo obtener una respuesta válida del backend.")
        return redirect(destino)

    if respuesta.status_code == 201:
        session.pop(CLAVE_COMPRA_PENDIENTE, None)

        return redirect(
            url_for(
                "compras.detalle_compra",
                id_compra=resultado["id"],
            )
        )

    flash(resultado.get("mensaje", "No se pudo confirmar la compra."))
    return redirect(destino)


@compras_bp.route("/compras/<int:id_compra>")
def detalle_compra(id_compra):
    token = session.get("token")
    if not verificar_cliente(token):
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

    compra = respuesta.json()

    # Comprueba si todavía se puede cancelar la compra.
    puede_cancelar = False

    if compra.get("estado") == "activa" and compra.get("funcion"):
        inicio = compra["funcion"].get("inicio")

        if inicio:
            try:
                inicio_funcion = datetime.fromisoformat(inicio)
                limite_cancelacion = datetime.now() + timedelta(hours=2)

                puede_cancelar = inicio_funcion >= limite_cancelacion

            except (TypeError, ValueError):
                puede_cancelar = False

    # Genera la imagen QR a partir del token original del backend.
    qr_imagen = None

    if compra.get("codigo_qr") and compra.get("estado") == "activa":
        imagen = qrcode.make(compra["codigo_qr"])

        buffer = io.BytesIO()
        imagen.save(buffer, format="PNG")

        qr_imagen = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

    return render_template(
        "compras/detalle.html",
        compra=compra,
        qr_imagen=qr_imagen,
        puede_cancelar=puede_cancelar,
    )


@compras_bp.route(
    "/compras/<int:id_compra>/cancelar",
    methods=["POST"],
)
def cancelar_compra(id_compra):
    token = session.get("token")
    if not verificar_cliente(token):
        return redirect(url_for("auth.login"))

    try:
        respuesta = requests.post(
            f"{BACKEND_URL}/compras/{id_compra}/cancelacion",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )

        resultado = respuesta.json()

    except (requests.RequestException, ValueError):
        flash("No se pudo obtener una respuesta del backend.")
        return redirect(
            url_for("compras.detalle_compra", id_compra=id_compra)
        )

    flash(resultado.get("mensaje", "No se pudo procesar la cancelación."))

    return redirect(
        url_for("compras.detalle_compra", id_compra=id_compra)
    )
