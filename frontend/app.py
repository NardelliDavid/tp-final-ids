from flask import Flask, redirect, url_for, session
from blueprints.peliculas import peliculas_bp
from blueprints.dashboard import dashboard_bp
from blueprints.funciones import funciones_bp
from blueprints.servicios import servicios_bp
from blueprints.auth import auth_bp
from blueprints.qr import qr_bp
from blueprints.compras import compras_bp

app = Flask(__name__, template_folder="templates")
app.secret_key = "clave-local-desarrollo"

app.register_blueprint(peliculas_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(funciones_bp)
app.register_blueprint(servicios_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(qr_bp)
app.register_blueprint(compras_bp)

@app.route("/")
def index():
    return redirect(url_for("auth.login_admin"))

if __name__ == "__main__":
    app.run(port=5001, debug=True)

