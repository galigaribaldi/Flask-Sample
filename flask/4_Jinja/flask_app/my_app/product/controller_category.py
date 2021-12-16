#from my_app import app
from flask import Blueprint, render_template, request, redirect, url_for, get_flashed_messages
from flask.helpers import flash
from sqlalchemy.sql.elements import not_
from flask_login import login_required
###
from my_app import db, rol_admin_need
from my_app.product.model.category import Category
from my_app.product.model.category import CategoryForm
category = Blueprint('category',__name__)

@category.before_request
@login_required
@rol_admin_need
def constructor():
    pass

@category.route("/")
@category.route("/category")
@category.route("/category/<int:page>")
def index(page=1):
    return render_template('category/index.html', categories = Category.query.paginate(page, 5))

@category.route('/category/<int:id>')
def show(id):
    print(id)
    category = Category.query.get_or_404(id)
    return render_template('category/show.html', categories = category)

@category.route('/test')
def test():
    p = Category.query.limit(2).all()
    print(p)
    p = Category.query.limit(2).first()
    print(p)
    p = Category.query.order_by(Category.id.desc()).limit(2).first()
    print(p)
    ###
    p = Category.query.filter_by(name="P1")
    print(p)
    ###
    p = Category.query.filter(Category.id>1).first()
    print(p)
    ###
    p = Category.query.filter_by(name = "P1", id=1).first()
    print(p)
    ###
    p = Category.query.filter(Category.name.like('%P%')).all()
    print(p)
    ###
    p = Category.query.filter(not_(Category.id > 1)).all()
    print(p)    
    ###Sólo se puede usar con la llave primaria
    p = Category.query.get({"id":1})
    print(p)
    return "flask"

@category.route('/test1')
def test1():
    p = Category("P5", 60.8, 3)
    db.session.add(p)
    db.session.commit()
    #db.session.commit()
    return "flask"
@category.route('/test2')
def test2():
    ##Actualizar
    p = Category.query.filter_by(id=1).first()
    p.name = "UP1"
    db.session.add(p)
    db.session.commit()
    #db.session.commit()
    return "flask"
@category.route('/test3')
def test3():
    ##Actualizar
    p = Category.query.filter_by(id=1).first()
    db.session.delete(p)
    db.session.commit()
    #db.session.commit()
    return "flask"

@category.route('/category-create', methods = ('GET', 'POST'))
def create():
    form = CategoryForm(meta={'csrf':False})
    if form.validate_on_submit():
        p = Category(request.form['name'],request.form['Id'])
        db.session.add(p)
        db.session.commit()
        flash("Categoria creado con exito")
        return redirect(url_for('category.create'))
    if form.errors:
        flash("Errores")
    return render_template('category/create.html', form=form)

@category.route('/category-insert', methods=["POST"])
def insert():
    print(request.form['name'],request.form['Precio'], request.form['Id'])
    p = Category(request.form['name'],request.form['Precio'], request.form['Id'])
    db.session.add(p)
    db.session.commit()
    flash("Categoryo creado con exito")
    return redirect(url_for('category.create'))

@category.route('/category-update/<int:id>',methods=["GET", "POST"])
def update(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm(meta={'csrf':False})
    print(category.products)
    if request.method == 'GET':
        form.name.data = category.name
        form.Id.data =id
    if form.validate_on_submit():
        ##Actualizar
        category.name =form.name.data
        db.session.add(category)
        db.session.commit()
        flash("Categoria Actualizado con exito")
        return redirect(url_for('category.update', id=category.id))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('category/update.html', category=category, form=form)

@category.route('/category-delete/<int:id>')
def delete(id=1):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash("Categoryo eliminado con extio")
    return redirect(url_for('category.index'))

@category.app_template_filter('iva')
def iva_filter(category):
    if category['price']:
        return category['price']* .20 + category["price"]
    else:
        return "No precio"