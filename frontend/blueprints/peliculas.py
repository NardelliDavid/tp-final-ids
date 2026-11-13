import requests
from flask import (Blueprint, render_template, request, session,
                   redirect, url_for, flash)
from config import BACKEND_URL

peliculas_bp = Blueprint("peliculas", __name__)


@peliculas_bp.route('/admin/peliculas')
def peliculas():
    token = session.get("token")
    if not token:
        return redirect(url_for("login_admin"))
    if session.get("usuario", {}).get("rol") != "administrador":
        return redirect(url_for("login_admin"))

    headers = {"Authorization": f"Bearer {token}"}
    respuesta = requests.get(
        f"{BACKEND_URL}/backoffice/peliculas",
        headers=headers,
        timeout=5
    )

    if respuesta.ok:
        resultado = respuesta.json()[0]['OK']
        lista = []
        for fila in resultado:
            lista.append({
                "id": fila[0],
                "id_api": fila[1],
                "titulo": fila[2],
                "sinopsis": fila[3],
                "poster": fila[4],
                "duracion": fila[5],
                "clasificacion": fila[6],
            })
        return render_template('admin/peliculas.html', peliculas=lista)
    else:
        return render_template('admin/peliculas.html', error=respuesta.status_code)


@peliculas_bp.route('/admin/eliminar_pelicula/<int:id_api>', methods=["POST"])
def eliminar_pelicula(id_api):
    token = session.get("token")
    if not token:
        return redirect(url_for("login_admin"))
    if session.get("usuario", {}).get("rol") != "administrador":
        return redirect(url_for("login_admin"))

    headers = {"Authorization": f"Bearer {token}"}
    respuesta = requests.delete(
        f"{BACKEND_URL}/backoffice/eliminar_pelicula_tmdb",
        json={"id": id_api},
        headers=headers,
        timeout=5
    )

    if respuesta.ok:
        flash("Película eliminada correctamente", "exito")
    else:
        try:
            mensaje = respuesta.json().get("Error", "No se pudo eliminar la película")
        except ValueError:
            mensaje = "No se pudo eliminar la película"
        flash(mensaje, "error")

    return redirect(url_for("peliculas.peliculas"))


@peliculas_bp.route('/admin/buscar_pelicula_tmdb', methods=["POST"])
def buscar_pelicula_tmdb():
    token = session.get("token")
    if not token:
        return redirect(url_for("login_admin"))
    if session.get("usuario", {}).get("rol") != "administrador":
        return redirect(url_for("login_admin"))

    titulo = request.form.get("titulo", "").strip()
    if not titulo:
        flash("Ingresá el título de la película.", "error")
        return redirect(url_for("peliculas.peliculas"))

    headers = {"Authorization": f"Bearer {token}"}
    respuesta = requests.post(
        f"{BACKEND_URL}/backoffice/buscar_peliculas_tmdb",
        json={"titulo": titulo},
        headers=headers,
        timeout=10
    )

    if not respuesta.ok:
        try:
            mensaje = respuesta.json().get("Error", "No se pudo buscar la película")
        except ValueError:
            mensaje = "No se pudo buscar la película"
        flash(mensaje, "error")
        return redirect(url_for("peliculas.peliculas"))

    return render_template('admin/buscar_pelicula.html', peliculas=respuesta.json())


@peliculas_bp.route('/admin/agregar_pelicula_tmdb', methods=["POST"])
def agregar_pelicula_tmdb():
    token = session.get("token")
    if not token:
        return redirect(url_for("login_admin"))
    if session.get("usuario", {}).get("rol") != "administrador":
        return redirect(url_for("login_admin"))

    id_tmdb = request.form.get("id_tmdb", type=int)
    headers = {"Authorization": f"Bearer {token}"}
    respuesta = requests.post(
        f"{BACKEND_URL}/backoffice/agregar_pelicula_tmdb",
        json={"id": id_tmdb},
        headers=headers,
        timeout=10
    )

    return render_template('admin/agregar_pelicula.html', respuesta=respuesta.json())