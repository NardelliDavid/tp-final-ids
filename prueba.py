from flask import Flask

app = Flask(__name__)


@app.route("/")
def inicio():
    return "¡Vas a poder hacer páginas webs!"


if __name__ == "__main__":
    app.run(debug=True)