from my_app import app

@app.route("/")
@app.route("/hola")
def hello_world():
    return "Hola Mundo en Flask  "