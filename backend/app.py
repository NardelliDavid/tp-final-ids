from flask import Flask
from backend.src.routes.Funciones import funciones_bp

app = Flask(__name__)

# GET /funciones/{id}/butacas
app.register_blueprint(funciones_bp)


if __name__ == "__main__":
    app.run(debug=True)