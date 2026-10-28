from flask import Flask, render_template
import requests

app = Flask(__name__, template_folder="src/templates")

@app.route("/")
def index():
    try:
        respuesta = requests.get("http://127.0.0.1:5000/", timeout=5)
        respuesta.raise_for_status()
        datos = respuesta.json()
    except:
        datos = {"mensaje": "No se pudo conectar con el backend"}
    return render_template("index.html", datos=datos)

if __name__ == "__main__":
    app.run(port=5001, debug=True)