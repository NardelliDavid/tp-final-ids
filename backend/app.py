from flask import Flask
from backend.src.routes.Funciones import funciones_bp
from backend.src.routes.Carteleras import carteleras_bp

app = Flask(__name__)

# Funciones
app.register_blueprint(funciones_bp)

# Carteleras
app.register_blueprint(carteleras_bp)

if __name__ == "__main__":
    app.run(debug=True)