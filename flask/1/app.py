"""
Aplicación mínima
---
Apicación minima de flask, que viene en los ejemplos

Notes
-----
Correr el código::
    1.- Teclear en la terminal: "FLASK_APP=app.py" y después: "flask run"
    2.- python3 app.py
    ¿Cual es la diferencia? si se ejecuta la forma 1, ésta usará la terminal integrada de Flask, mientras que ene l otro caso, sólo se correrá con el
    interprete de python.

Activar el modo development o debug::
    1.- Escribir en la terminal: "export FLASK_APP=my_application"
    2.- export FLASK_ENV=development
    3.- flask run --reload
    4.- flask run --no-reload
    5.- Opcionalmente se puede poner "app.run(debug=True)", la diferencia es la misma que arriba

"""
from flask import Flask, url_for, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/hola")
def hello_world():
    return "Hola Mundo en Flask  "

@app.route("/saludar")
@app.route("/saludar/<h1>")
@app.route("/saludar/<h1>/<lang>")
def saludar(h1="Cadena Vacia", lang="es"):
    return "Mensaje: "+ str(h1) + str(lang)

@app.route('/primerHtml/<name>')
@app.route('/primerHtml')
def primerHtml(name=""):
    return """
    <h1> Titulo %s</h1>
    """%name

@app.route('/staticFile')
def staticFile():
    #return "<img src='/static/img/FlaskLogo.png'>"
    return "<img src='"+url_for("static", filename="img/FlaskLogo.png")+"'>"

@app.route('/miPrimerTemplate/<name>')
@app.route('/miPrimerTemplate')
def miPrimerTempalte(name=""):
    #return "<img src='/static/img/FlaskLogo.png'>"
    return render_template("view.html", name=name)

if __name__ == "__main__":
    """
    Para activar el modo debug poner: "app.run(debug=True)"
    """
    #app.run(debug=True)
    app.run()
    