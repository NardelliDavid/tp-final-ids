from flask import Blueprint, render_template, session, redirect, url_for

servicios_bp = Blueprint("servicios", __name__)

@servicios_bp.route('/admin/servicios')
def servicios():
    if not session.get("token"):
        return redirect(url_for("login_admin"))
    if session.get("usuario", {}).get("rol") != "administrador":
        return redirect(url_for("login_admin"))
    return render_template('admin/servicios.html')