from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, logout_user
from functools import wraps
app = Flask(__name__)

app.config.from_object('configuration.DevelopmentConfig')
db = SQLAlchemy(app)

###Módulo de Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "fauth.login"
###Decorador
def rol_admin_need(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if current_user.rol.value != "admin":
            logout_user()
            return redirect(url_for('fauth.login'))
        return f(*args, **kwds)
    return wrapper
from my_app.product.controller_product import product
from my_app.product.controller_category import category
#from my_app.auth.views_controller import auth
from my_app.fauth.views_controller import fauth

##rest
from my_app.rest_api.product_api import product_view
from my_app.rest_api.category_api import category_view

app.register_blueprint(product)
app.register_blueprint(category)
#app.register_blueprint(auth)
app.register_blueprint(fauth)
db.create_all()


## Registrar filtros
@app.template_filter('mydouble')
def mydouble_filter(n:int):
    return n*2