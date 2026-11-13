from flask import Blueprint, render_template, session, redirect, url_for

funciones_bp = Blueprint("funciones", __name__)

@funciones_bp.route('/admin/funciones')
def funciones():
    if not session.get("token"):
        return redirect(url_for("login_admin"))
    if session.get("usuario", {}).get("rol") != "administrador":
        return redirect(url_for("login_admin"))
    return render_template('admin/funciones.html')