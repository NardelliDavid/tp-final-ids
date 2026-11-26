import os
import io
import base64
import html
import requests
import qrcode

from datetime import datetime
from decimal import Decimal
from dotenv import load_dotenv


load_dotenv()


def escapar(valor):
    if valor is None:
        return ""
    return html.escape(str(valor))


def formatear_precio(valor):
    try:
        numero = Decimal(str(valor or 0))
        return f"${numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "$0,00"


def formatear_fecha(valor):
    if not valor:
        return "No disponible"

    try:
        fecha = datetime.fromisoformat(str(valor).replace("Z", "+00:00"))
        return fecha.strftime("%d/%m/%Y %H:%M")
    except (ValueError, TypeError):
        return escapar(valor)


def enviar_comprobante(compra, destinatario):
    api_key = os.getenv("BREVO_API_KEY")
    remitente = os.getenv("BREVO_REMITENTE")
    nombre_remitente = os.getenv("BREVO_NOMBRE", "Cine Paradiso")

    if not api_key or not remitente:
        raise ValueError("Falta configurar Brevo en el archivo .env")

    codigo_qr = compra.get("codigo_qr")

    if not codigo_qr:
        raise ValueError("La compra no tiene un código QR")

    funcion = compra.get("funcion", {})
    entradas = compra.get("entradas", [])
    servicios = compra.get("servicios", [])

    # Generar el código QR
    imagen = qrcode.make(codigo_qr)
    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    # Preparar las entradas
    filas_entradas = ""

    for entrada in entradas:
        filas_entradas += f"""
        <tr>
            <td style="padding:12px;border-bottom:1px solid #eeeeee;">
                <strong>{escapar(entrada.get("butaca"))}</strong>
            </td>
            <td align="right" style="padding:12px;border-bottom:1px solid #eeeeee;">
                {formatear_precio(entrada.get("precio"))}
            </td>
        </tr>
        """

    # Preparar los servicios adicionales
    filas_servicios = ""

    for servicio in servicios:
        filas_servicios += f"""
        <tr>
            <td style="padding:12px;border-bottom:1px solid #eeeeee;">
                {escapar(servicio.get("nombre"))}
            </td>
            <td align="center" style="padding:12px;border-bottom:1px solid #eeeeee;">
                {escapar(servicio.get("cantidad"))}
            </td>
            <td align="right" style="padding:12px;border-bottom:1px solid #eeeeee;">
                {formatear_precio(servicio.get("subtotal"))}
            </td>
        </tr>
        """

    if not filas_servicios:
        filas_servicios = """
        <tr>
            <td colspan="3" style="padding:12px;color:#777777;">
                No se agregaron servicios adicionales.
            </td>
        </tr>
        """

    compra_id = escapar(compra.get("id"))
    pelicula = escapar(funcion.get("pelicula"))
    cine = escapar(funcion.get("local"))
    sala = escapar(funcion.get("sala"))
    inicio = formatear_fecha(funcion.get("inicio"))
    fin = formatear_fecha(funcion.get("fin"))
    total = formatear_precio(compra.get("total"))

    # Diseño del comprobante
    contenido_html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Comprobante Cine Paradiso</title>
    </head>

    <body style="
        margin:0;
        padding:0;
        background-color:#f2f3f5;
        font-family:Arial,Helvetica,sans-serif;
        color:#252b36;
    ">

        <table width="100%" cellpadding="0" cellspacing="0"
               style="background-color:#f2f3f5;padding:30px 10px;">

            <tr>
                <td align="center">

                    <table width="600" cellpadding="0" cellspacing="0"
                           style="
                               max-width:600px;
                               width:100%;
                               background-color:#ffffff;
                               border-radius:12px;
                               overflow:hidden;
                           ">

                        <!-- ENCABEZADO -->
                        <tr>
                            <td align="center"
                                style="
                                    background-color:#17243d;
                                    padding:35px 20px;
                                    color:#ffffff;
                                ">

                                <h1 style="
                                    margin:0;
                                    font-size:29px;
                                    letter-spacing:3px;
                                    color:#ffffff;
                                ">
                                    CINE PARADISO
                                </h1>

                                <p style="
                                    margin:10px 0 0;
                                    font-size:11px;
                                    letter-spacing:2px;
                                    color:#d5dcec;
                                ">
                                    TU EXPERIENCIA COMIENZA AQUÍ
                                </p>

                                <div style="
                                    display:inline-block;
                                    margin-top:22px;
                                    padding:9px 18px;
                                    border-radius:20px;
                                    background-color:#d9b56d;
                                    color:#17243d;
                                    font-size:11px;
                                    font-weight:bold;
                                    letter-spacing:1px;
                                ">
                                    COMPRA CONFIRMADA
                                </div>

                            </td>
                        </tr>

                        <!-- MENSAJE PRINCIPAL -->
                        <tr>
                            <td style="padding:30px 30px 15px;">

                                <h2 style="
                                    margin:0 0 10px;
                                    font-size:24px;
                                    color:#17243d;
                                ">
                                    ¡Gracias por tu compra!
                                </h2>

                                <p style="
                                    margin:0;
                                    color:#737987;
                                    font-size:14px;
                                    line-height:1.6;
                                ">
                                    Tu compra fue registrada correctamente.
                                    A continuación encontrarás todos los
                                    detalles de tu función.
                                </p>

                            </td>
                        </tr>

                        <!-- NUMERO DE COMPRA -->
                        <tr>
                            <td style="padding:15px 30px;">

                                <table width="100%" cellpadding="0" cellspacing="0"
                                       style="
                                           background-color:#f5f6f8;
                                           border-radius:8px;
                                       ">
                                    <tr>
                                        <td style="padding:16px;">
                                            <span style="
                                                font-size:11px;
                                                color:#777f8d;
                                                letter-spacing:1px;
                                            ">
                                                COMPROBANTE DE COMPRA
                                            </span>

                                            <div style="
                                                margin-top:5px;
                                                font-size:20px;
                                                font-weight:bold;
                                                color:#17243d;
                                            ">
                                                Nº {compra_id}
                                            </div>
                                        </td>
                                    </tr>
                                </table>

                            </td>
                        </tr>

                        <!-- PELICULA -->
                        <tr>
                            <td style="padding:15px 30px;">

                                <h3 style="
                                    margin:0 0 15px;
                                    font-size:17px;
                                    color:#17243d;
                                ">
                                    Detalles de la función
                                </h3>

                                <div style="
                                    padding:20px;
                                    border:1px solid #e7e9ed;
                                    border-radius:9px;
                                ">

                                    <h2 style="
                                        margin:0 0 18px;
                                        font-size:21px;
                                        color:#17243d;
                                    ">
                                        {pelicula}
                                    </h2>

                                    <p style="margin:9px 0;font-size:14px;">
                                        <strong>Cine:</strong> {cine}
                                    </p>

                                    <p style="margin:9px 0;font-size:14px;">
                                        <strong>Sala:</strong> {sala}
                                    </p>

                                    <p style="margin:9px 0;font-size:14px;">
                                        <strong>Inicio:</strong> {inicio}
                                    </p>

                                    <p style="margin:9px 0;font-size:14px;">
                                        <strong>Finalización:</strong> {fin}
                                    </p>

                                </div>

                            </td>
                        </tr>

                        <!-- ENTRADAS -->
                        <tr>
                            <td style="padding:15px 30px;">

                                <h3 style="
                                    margin:0 0 12px;
                                    font-size:17px;
                                    color:#17243d;
                                ">
                                    Tus entradas
                                </h3>

                                <table width="100%" cellpadding="0" cellspacing="0"
                                       style="
                                           border:1px solid #eeeeee;
                                           border-radius:8px;
                                           font-size:14px;
                                       ">
                                    <tr style="background-color:#f5f6f8;">
                                        <th align="left" style="padding:12px;">
                                            Butaca
                                        </th>
                                        <th align="right" style="padding:12px;">
                                            Precio
                                        </th>
                                    </tr>

                                    {filas_entradas}

                                </table>

                            </td>
                        </tr>

                        <!-- SERVICIOS -->
                        <tr>
                            <td style="padding:15px 30px;">

                                <h3 style="
                                    margin:0 0 12px;
                                    font-size:17px;
                                    color:#17243d;
                                ">
                                    Servicios adicionales
                                </h3>

                                <table width="100%" cellpadding="0" cellspacing="0"
                                       style="
                                           border:1px solid #eeeeee;
                                           border-radius:8px;
                                           font-size:13px;
                                       ">
                                    <tr style="background-color:#f5f6f8;">
                                        <th align="left" style="padding:12px;">
                                            Servicio
                                        </th>
                                        <th align="center" style="padding:12px;">
                                            Cant.
                                        </th>
                                        <th align="right" style="padding:12px;">
                                            Subtotal
                                        </th>
                                    </tr>

                                    {filas_servicios}

                                </table>

                            </td>
                        </tr>

                        <!-- TOTAL -->
                        <tr>
                            <td style="padding:20px 30px;">

                                <table width="100%" cellpadding="0" cellspacing="0"
                                       style="
                                           background-color:#17243d;
                                           border-radius:9px;
                                       ">
                                    <tr>
                                        <td style="
                                            padding:20px;
                                            color:#ffffff;
                                            font-size:14px;
                                            font-weight:bold;
                                        ">
                                            TOTAL DE LA COMPRA
                                        </td>

                                        <td align="right" style="
                                            padding:20px;
                                            color:#e5c47f;
                                            font-size:22px;
                                            font-weight:bold;
                                        ">
                                            {total}
                                        </td>
                                    </tr>
                                </table>

                            </td>
                        </tr>

                        <!-- QR -->
                        <tr>
                            <td align="center" style="padding:25px 30px;">

                                <h3 style="
                                    margin:0 0 10px;
                                    font-size:19px;
                                    color:#17243d;
                                ">
                                    Tu entrada digital
                                </h3>

                                <p style="
                                    margin:0 0 15px;
                                    color:#737987;
                                    font-size:13px;
                                    line-height:1.6;
                                ">
                                    Adjuntamos tu código QR.
                                    Presentalo al ingresar al cine.
                                </p>

                                <div style="
                                    padding:15px;
                                    border:1px dashed #d9b56d;
                                    border-radius:10px;
                                    display:inline-block;
                                ">
                                    <strong style="
                                        color:#17243d;
                                        font-size:13px;
                                    ">
                                        CÓDIGO QR ADJUNTO
                                    </strong>
                                </div>

                            </td>
                        </tr>

                        <!-- PIE -->
                        <tr>
                            <td align="center" style="
                                background-color:#17243d;
                                padding:28px 20px;
                                color:#ffffff;
                            ">

                                <h3 style="
                                    margin:0 0 8px;
                                    color:#ffffff;
                                    font-size:17px;
                                    letter-spacing:1px;
                                ">
                                    ¡Que disfrutes la función!
                                </h3>

                                <p style="
                                    margin:0;
                                    color:#cbd3e1;
                                    font-size:12px;
                                ">
                                    Equipo de Cine Paradiso
                                </p>

                                <p style="
                                    margin:18px 0 0;
                                    color:#8995aa;
                                    font-size:10px;
                                ">
                                    Este correo fue generado automáticamente.
                                    No es necesario responderlo.
                                </p>

                            </td>
                        </tr>

                    </table>

                </td>
            </tr>
        </table>

    </body>
    </html>
    """

    texto_plano = f"""
CINE PARADISO

¡Gracias por tu compra!

Comprobante Nº {compra_id}

Película: {pelicula}
Cine: {cine}
Sala: {sala}
Inicio: {inicio}
Finalización: {fin}

Total: {total}

Adjuntamos tu código QR.
Presentalo al ingresar al cine.

¡Que disfrutes la función!
Equipo de Cine Paradiso.
"""

    datos = {
        "sender": {
            "name": nombre_remitente,
            "email": remitente
        },
        "to": [
            {
                "email": destinatario
            }
        ],
        "subject": f"Tu entrada para {pelicula} - Cine Paradiso",
        "htmlContent": contenido_html,
        "textContent": texto_plano,
        "attachment": [
            {
                "name": f"codigo-qr-compra-{compra_id}.png",
                "content": qr_base64
            }
        ]
    }

    respuesta = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        },
        json=datos,
        timeout=30
    )

    respuesta.raise_for_status()

    return True
