from flask.views import  MethodView
from flask import request
from my_app.product.model.product import Product
from my_app.rest_api.helper.request import sendResJson
from my_app import app, db
import json

class ProductApi(MethodView):
    def get(self, id=None):
        if id:
            products = Product.query.get(id)
            res = {
                'id':products.id,
                'name':products.name
            }
            res = productToJson(products)
        else:
            res = []
            products = Product.query.all()
            for p in products:
                res.append(productToJson(p))
        return sendResJson(res, None, 200)
    
    def delete(self, id):
        product = Product.query.get(id)
        
        if not product:
            return sendResJson(None, "Producto no existe", 403)
        db.session.delete(product)
        db.session.commit()
        return sendResJson(None,"Producto Eliminado", 200)
    
    def post(self):
        if not request.form:
            return sendResJson(None, "Sin parametros", 403)
        ##Nombre
        if not "name" in request.form or len(request.form["name"])<3:
            return sendResJson(None, "Nombre no valido", 403)
        ##Precio
        if not "price" in request.form:
            return sendResJson(None, "Precio no Valido", 403)
        try:
            float(request.form['price'])
        except ValueError:
            return sendResJson(None, "Precio No Valido", 403)
        ##Categoria
        if not "category_id" in request.form:
            return sendResJson(None, "Category Id no valido", 403)
        try:
            int(request.form['category_id'])
        except ValueError:
            return sendResJson(None, "Categoria no valida", 403)
        p = Product(request.form['name'],request.form['price'], request.form['id'],request.form['category_id'])
        db.session.add(p)
        db.session.commit()
        return sendResJson(productToJson(p),"Creado con exito", 200)
    
    def put(self, id):
        p = Product.query.get(id)
        print(p)
        print(request.form)
        if not p:
            return sendResJson(None, "Producto no existe",403)
        
        if not "name" in request.form or len(request.form["name"])<3:
            return sendResJson(None, "Nombre no valido 1", 403)
        ##Precio
        if not "price" in request.form:
            return sendResJson(None, "Precio no Valido", 403)
        try:
            float(request.form['price'])
        except ValueError:
            return sendResJson(None, "Precio No Valido", 403)
        ##Categoria
        if not "category_id" in request.form:
            return sendResJson(None, "Category Id no valido", 403)
        try:
            int(request.form['category_id'])
        except ValueError:
            return sendResJson(None, "Categoria no valida", 403)
        p.name, p.price, p.category_id = request.form['name'],request.form['price'],request.form['category_id']
        db.session.add(p)
        db.session.commit()
        return sendResJson(productToJson(p),"Creado con exito", 200)        

def productToJson(product: Product):
    return {
        'id':product.id,
        'name':product.name,
        'category_id': product.category_id,
        'category': product.category.name,
        }

product_view = ProductApi.as_view('product_view')
app.add_url_rule(
    '/api/products/',
    view_func=product_view,
    methods = ['GET', 'POST']
    )

app.add_url_rule(
    '/api/products/<int:id>',
    view_func=product_view,
    methods = ['GET','DELETE','PUT']
    )