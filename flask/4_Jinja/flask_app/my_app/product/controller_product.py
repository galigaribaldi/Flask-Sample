#from my_app import app
from flask import Blueprint, render_template, request, redirect, url_for, get_flashed_messages
from flask.helpers import flash
from sqlalchemy.sql.elements import not_
###
from my_app import db
from my_app.product.model.products import PRODUCTS
from my_app.product.model.product import Product
from my_app.product.model.category import Category
from my_app.product.model.product import ProductForm
product = Blueprint('product',__name__)

@product.route("/")
@product.route("/product")
@product.route("/product/<int:page>")
def index(page=1):
    return render_template('product/index.html', products = Product.query.paginate(page, 5))

@product.route('/product/<int:id>')
def show(id):
    print(id)
    product = Product.query.get_or_404(id)
    return render_template('product/show.html', products = product)

@product.route('/test')
def test():
    p = Product.query.limit(2).all()
    print(p)
    p = Product.query.limit(2).first()
    print(p)
    p = Product.query.order_by(Product.id.desc()).limit(2).first()
    print(p)
    ###
    p = Product.query.filter_by(name="P1")
    print(p)
    ###
    p = Product.query.filter(Product.id>1).first()
    print(p)
    ###
    p = Product.query.filter_by(name = "P1", id=1).first()
    print(p)
    ###
    p = Product.query.filter(Product.name.like('%P%')).all()
    print(p)
    ###
    p = Product.query.filter(not_(Product.id > 1)).all()
    print(p)    
    ###Sólo se puede usar con la llave primaria
    p = Product.query.get({"id":1})
    print(p)
    return "flask"

@product.route('/test1')
def test1():
    p = Product("P5", 60.8, 3)
    db.session.add(p)
    db.session.commit()
    #db.session.commit()
    return "flask"
@product.route('/test2')
def test2():
    ##Actualizar
    p = Product.query.filter_by(id=1).first()
    p.name = "UP1"
    db.session.add(p)
    db.session.commit()
    #db.session.commit()
    return "flask"
@product.route('/test3')
def test3():
    ##Actualizar
    p = Product.query.filter_by(id=1).first()
    db.session.delete(p)
    db.session.commit()
    #db.session.commit()
    return "flask"

@product.route('/product-create', methods = ('GET', 'POST'))
def create():
    form = ProductForm(meta={'csrf':False})
    ###Opciones de relaciones
    categories = [(c.id, c.name) for c in Category.query.all()]
    print("\n\n\n",categories)
    form.category_id.choices = categories
    
    if form.validate_on_submit():
        
        print("Name:", request.form['name'],"precio: ",request.form['price'], "ID:", request.form['Id'],"Categoria: ",request.form['category_id'])
        p = Product(request.form['name'],request.form['price'], request.form['Id'],request.form['category_id'])
        db.session.add(p)
        db.session.commit()
        flash("Producto creado con exito")
        return redirect(url_for('product.create'))
    if form.errors:
        flash("Errores")
    return render_template('product/create.html', form=form)

@product.route('/product-insert', methods=["POST"])
def insert():
    print(request.form['name'],request.form['Precio'], request.form['Id'])
    p = Product(request.form['name'],request.form['Precio'], request.form['Id'])
    db.session.add(p)
    db.session.commit()
    flash("Producto creado con exito")
    return redirect(url_for('product.create'))

@product.route('/product-update/<int:id>',methods=["GET", "POST"])
def update(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(meta={'csrf':False})
    categories = [(c.id, c.name) for c in Category.query.all()]
    form.category_id.choices = categories
    if request.method == 'GET':
        form.name.data = product.name
        form.category_id.data = product.category_id
        form.Id.data =id
    if form.validate_on_submit():
        ##Actualizar
        product.name =form.name.data
        #product.price = form.price.data
        product.category_id = form.category_id.data
        db.session.add(product)
        db.session.commit()
        flash("Producto Actualizado con exito")
        return redirect(url_for('product.update', id=product.id))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('product/update.html', product=product, form=form)

@product.route('/product-delete/<int:id>')
def delete(id=1):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Producto eliminado con extio")
    return redirect(url_for('product.index'))

@product.app_template_filter('iva')
def iva_filter(product):
    if product['price']:
        return product['price']* .20 + product["price"]
    else:
        return "No precio"