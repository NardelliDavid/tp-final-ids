import requests
from flask import (
    Blueprint, render_template, request, session,
    redirect, url_for, flash, abort
)
from config import BACKEND_URL
from utils import *

peliculas_bp = Blueprint("peliculas", __name__)

@peliculas_bp.route('/admin/peliculas')
def peliculas():
    token = session.get("token")
    if not verificar_administrador(token):
        return redirect(url_for("auth.login_admin"))
    
    try:
        respuesta = requests.get(
            f"{BACKEND_URL}/backoffice/peliculas",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )

        if respuesta.ok:
            resultado = respuesta.json()[0]["OK"]

            lista = []

            for fila in resultado:
                lista.append({
                    "id": fila[0],
                    "id_api": fila[1],
                    "titulo": fila[2],
                    "sinopsis": fila[3],
                    "poster": fila[4],
                    "duracion": fila[5],
                    "clasificacion": fila[6]
                })

            return render_template(
                "admin/peliculas.html",
                peliculas=lista
            )

        flash("No se pudieron cargar las películas.", "error")

    except requests.RequestException:
        flash("No se pudo conectar con el servidor.", "error")

    return render_template(
        "admin/peliculas.html",
        peliculas=[]
    )


@peliculas_bp.route('/admin/importar_peliculas')
def importar_peliculas():
    if not verificar_administrador(session.get("token")):
        return redirect(url_for("auth.login_admin"))

    return render_template(
        "admin/buscar_pelicula.html",
        peliculas=[],
        busqueda=""
    )


@peliculas_bp.route('/admin/eliminar_pelicula/<int:id_api>', methods=["POST"])
def eliminar_pelicula(id_api):
    token = session.get("token")
    if not verificar_administrador(token):
        return redirect(url_for("auth.login_admin"))

    try:
        respuesta = requests.delete(
            f"{BACKEND_URL}/backoffice/eliminar_pelicula_tmdb",
            json={"id": id_api},
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )

        if respuesta.ok:
            flash("Película eliminada correctamente.", "exito")
        else:
            try:
                mensaje = respuesta.json().get(
                    "Error",
                    "No se pudo eliminar la película."
                )
            except ValueError:
                mensaje = "No se pudo eliminar la película."

            flash(mensaje, "error")

    except requests.RequestException:
        flash("No se pudo conectar con el servidor.", "error")

    return redirect(url_for("peliculas.peliculas"))


@peliculas_bp.route('/admin/buscar_pelicula_tmdb', methods=["POST"])
def buscar_pelicula_tmdb():
    token = session.get("token")
    if not verificar_administrador(token):
        return redirect(url_for("auth.login_admin"))

    titulo = request.form.get("titulo", "").strip()

    if not titulo:
        flash("Ingresá el título de la película.", "error")
        return redirect(url_for("peliculas.importar_peliculas"))

    try:
        respuesta = requests.post(
            f"{BACKEND_URL}/backoffice/buscar_peliculas_tmdb",
            json={"titulo": titulo},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )

        if not respuesta.ok:
            try:
                mensaje = respuesta.json().get(
                    "Error",
                    "No se pudo buscar la película."
                )
            except ValueError:
                mensaje = "No se pudo buscar la película."

            flash(mensaje, "error")

            return render_template(
                "admin/buscar_pelicula.html",
                peliculas=[],
                busqueda=titulo
            )

        return render_template(
            "admin/buscar_pelicula.html",
            peliculas=respuesta.json(),
            busqueda=titulo
        )

    except requests.RequestException:
        flash("No se pudo conectar con TMDB.", "error")

        return render_template(
            "admin/buscar_pelicula.html",
            peliculas=[],
            busqueda=titulo
        )


@peliculas_bp.route('/admin/agregar_pelicula_tmdb', methods=["POST"])
def agregar_pelicula_tmdb():
    token = session.get("token")
    if not verificar_administrador(token):
        return redirect(url_for("auth.login_admin"))

    id_tmdb = request.form.get("id_tmdb", type=int)

    if not id_tmdb:
        flash("Seleccioná una película válida.", "error")
        return redirect(url_for("peliculas.importar_peliculas"))

    try:
        respuesta = requests.post(
            f"{BACKEND_URL}/backoffice/agregar_pelicula_tmdb",
            json={"id": id_tmdb},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )

        return render_template(
            "admin/agregar_pelicula.html",
            respuesta=respuesta.json()
        )

    except requests.RequestException:
        flash("No se pudo conectar con el servidor.", "error")

        return redirect(url_for("peliculas.importar_peliculas"))
