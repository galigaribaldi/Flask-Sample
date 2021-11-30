#from my_app import app
from flask import Blueprint

hello = Blueprint('hello_world',__name__)

@hello.route("/")
@hello.route("/hola")
def fhello_world():
    return "Hola Mundo en Flask  "