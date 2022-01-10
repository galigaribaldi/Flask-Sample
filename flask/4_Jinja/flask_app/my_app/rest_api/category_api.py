from flask.views import  MethodView
from flask import request
from my_app.product.model.category import Category
from my_app.rest_api.helper.request import sendResJson
from my_app import app, db
import json

class CategoryApi(MethodView):
    def get(self, id=None):
        if id:
            ccategories = Category.query.get(id)
            res = {
                'id':ccategories.id,
                'name':ccategories.name
            }
            res = categoryToJson(ccategories)
        else:
            res = []
            ccategories = Category.query.all()
            print(ccategories)
            for p in ccategories:
                res.append(categoryToJson(p))
        return sendResJson(res, None, 200)
    
    def delete(self, id):
        product = Category.query.get(id)
        
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
        p = Category(request.form['name'],request.form['price'], request.form['id'],request.form['category_id'])
        db.session.add(p)
        db.session.commit()
        return sendResJson(categoryToJson(p),"Creado con exito", 200)
    
    def put(self, id):
        p = Category.query.get(id)
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
        return sendResJson(categoryToJson(p),"Creado con exito", 200)        

def categoryToJson(category: Category):
    return {
        'id':category.id,
        'name':category.name
        }

category_view = CategoryApi.as_view('category_view')
app.add_url_rule(
    '/api/categories/',
    view_func=category_view,
    methods = ['GET', 'POST']
    )

app.add_url_rule(
    '/api/categories/<int:id>',
    view_func=category_view,
    methods = ['GET','DELETE','PUT']
    )