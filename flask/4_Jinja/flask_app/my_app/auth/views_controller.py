from os import name
from flask import Blueprint, session,render_template, request, redirect, url_for, flash
###
from my_app import db
###
from my_app.auth.model.user import User, LoginForm, RegisterForm
auth = Blueprint('auth',__name__)

@auth.route('/register', methods = ('GET', 'POST'))
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

@auth.route('/login', methods = ('GET', 'POST'))
def login():
    form = LoginForm(meta={'csrf':False})
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user and user.check_password(form.password.data):
            ##Registrar la sesion
            session['username'] = user.username
            session['rol'] = user.rol.value
            flash("Bienvenido de nuevo: "+ user.username)
            return redirect(url_for('product.index'))
        else:
            flash("Contraseña o correo incorrecto",'danger')
        if form.errors:
            flash("Errores")
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
    session.pop('username')
    session.pop('rol')
    return redirect(url_for('auth.login'))
    