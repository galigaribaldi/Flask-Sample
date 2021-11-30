#from my_app import app
from flask import Blueprint

hello2 = Blueprint('hello_world2',__name__)

@hello2.route("/2")
@hello2.route("/hola2")
def hello_world2():
    return "Hola Mundo en Flask  2"