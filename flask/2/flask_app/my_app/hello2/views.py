from my_app import app

@app.route("/2")
@app.route("/hola2")
def hello_world2():
    return "Hola Mundo en Flask  2"