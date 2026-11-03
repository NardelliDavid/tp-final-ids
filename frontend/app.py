from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")
app.secret_key = "clave-local-desarrollo"

@app.route('/')
def dashboard():
    return render_template('admin/dashboard.html')

if __name__== "__main__":
    app.run(port=5001, debug=True)

