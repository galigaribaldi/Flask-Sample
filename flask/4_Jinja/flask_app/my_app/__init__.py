from flask import Flask
from my_app.product.views import product
#from my_app.hello2.views import hello
app = Flask(__name__)

app.register_blueprint(product)

## Registrar filtros
@app.template_filter('mydouble')
def mydouble_filter(n:int):
    return n*2