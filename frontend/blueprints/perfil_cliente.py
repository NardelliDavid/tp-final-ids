from flask import Blueprint, flash, redirect, render_template, request, session, url_for

perfil_cliente_bp = Blueprint("perfil_cliente", __name__)

@perfil_cliente_bp.route("/mi_perfil")
def mi_perfil():
    return render_template('cartelera/mi_perfil.html')