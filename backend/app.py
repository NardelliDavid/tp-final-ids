# archivo que arranca el servidor Flask en el puerto 5000. Sufunción es crear la aplicación, registrar todos los grupos de rutas (Blueprints) y dejar el servidor escuchando peticiones HTTP.
from flask import Flask

from src.routes.QR import qr_bp
from src.routes.servicios import servicios_bp
from src.routes.validar import auth_bp
from src.routes.perfil import perfil_bp
from src.routes.peliculas import peliculas_bp
from src.routes.dashboard import dashboard_bp
from src.routes.Funciones import funciones_bp
from src.routes.Carteleras import carteleras_bp
from src.routes.compras import compras_bp

app = Flask(__name__)
app.register_blueprint(servicios_bp)

app.register_blueprint(qr_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(peliculas_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(funciones_bp)
app.register_blueprint(carteleras_bp)
app.register_blueprint(compras_bp)

#Garantiza que el servidor (app.run()) solo arranque si ejecutamos python app.py directamente, y no si otro archivo importa app
if __name__ == "__main__":
# hace que el servidor se reinicie automáticamente cada vez que guardamos un cambio    
    app.run(debug=True)
