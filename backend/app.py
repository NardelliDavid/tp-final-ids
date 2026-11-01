from flask import Flask, jsonify
from db.conexion_db import conexion

from src.routes.validar import auth_bp
from src.routes.perfil import perfil_bp
from src.routes.peliculas import peliculas_bp
from src.routes.dashboard import dashboard_bp
from src.routes.Funciones import funciones_bp
from src.routes.Carteleras import carteleras_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(peliculas_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(funciones_bp)
app.register_blueprint(carteleras_bp)

@app.route("/")
def index():
    try:
        conn = conexion()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM peliculas;")
        consulta = cursor.fetchall()

        cursor.close()
        conn.close()

        resultado = jsonify(consulta), 200
    except Exception as e:
        resultado = jsonify({"mensaje": str(e)}), 500

    return resultado

if __name__ == "__main__":
    app.run(debug=True)
