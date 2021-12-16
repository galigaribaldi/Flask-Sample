from flask import Blueprint, session,render_template, request, redirect, url_for, flash
import flask
###
from my_app import db, login_manager
from flask_login import login_user,logout_user,current_user,login_required
###
from my_app.auth.model.user import User, LoginForm, RegisterForm
fauth = Blueprint('fauth',__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@fauth.route('/register', methods = ('GET', 'POST'))
def register():
    form = RegisterForm(meta={'csrf':False})
    if form.validate_on_submit():
        if User.query.filter_by(username=form.name.data).first():
            flash("El usuario ya existe en el sistema",'danger')
        else:
            ###Crear usuario
            p = User(form.name.data,
                    form.password.data,
                    form.Id.data)
            db.session.add(p)
            db.session.commit()
            flash("Usuario creado con exito")
            return redirect(url_for('auth.register'))
        if form.errors:
            flash("Errores")
    return render_template('auth/register.html', form=form)

@fauth.route('/login', methods = ('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        flash("Ya estas autenticado prro")
        return redirect(url_for('product.index'))
    form = LoginForm(meta={'csrf':False})
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user and user.check_password(form.password.data):
            ##Registrar la sesion
            print(user, type(user))
            login_user(user)
            ###
            flash("Bienvenido de nuevo: "+ user.username)
            ##
            next = request.form['next']
            #if not is_safe_url(next):
            #    return flask.abort(400)
            print(next)
            return redirect(next or url_for('product.index'))
        else:
            flash("Contraseña o correo incorrecto",'danger')
        if form.errors:
            flash("Errores")
    return render_template('auth/login.html', form=form)

@fauth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('fauth.login'))
    
    
@fauth.route('/protegido')
@login_required
def protegido():
    return "Vusta protegida"