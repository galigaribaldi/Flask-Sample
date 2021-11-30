from flask import Flask
from my_app.hello1.views import hello
#from my_app.hello2.views import hello
app = Flask(__name__)

app.register_blueprint(hello)

##importar las vistas
#import my_app.hello1.views
#import my_app.hello2.views