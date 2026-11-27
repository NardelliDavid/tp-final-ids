import requests
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from config import BACKEND_URL
from utils import *

carteleras_bp = Blueprint("carteleras", __name__)

@carteleras_bp.route("/index")
def index():
    token = session.get("token")
    if not verificar_cliente(token):
        return redirect(url_for("auth.login"))

    respuesta = requests.get(
                f"{BACKEND_URL}/cartelera",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10
            )
    
    return render_template("cartelera/index.html", cartelera=respuesta.json())

@carteleras_bp.route("/pelicula/<int:pelicula_id>/funciones")
def funciones_pelicula(pelicula_id):
    token = session.get("token")
    if not verificar_cliente(token):
        return redirect(url_for("auth.login"))

    respuesta = requests.get(
        f"{BACKEND_URL}/peliculas/{pelicula_id}/funciones",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10
    )

    if respuesta.status_code == 404:
        return redirect(url_for('carteleras.index'))

    if respuesta.status_code != 200:
        return redirect(url_for('carteleras.index'))

    datos = respuesta.json()

    return render_template(
        "cartelera/funciones.html",
        pelicula=datos["pelicula"],
        funciones=datos["funciones"]
    )