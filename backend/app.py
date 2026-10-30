from flask import Flask, jsonify
from db.conexion_db import conexion
from src.routes.servicios import servicios_bp

app = Flask(__name__)
app.register_blueprint(servicios_bp)

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
    app.run(port=5000, debug=True)