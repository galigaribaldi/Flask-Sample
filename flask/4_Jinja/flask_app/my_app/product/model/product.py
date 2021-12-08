from my_app import db
from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField,SelectField
from wtforms.validators import InputRequired, NumberRange

class Product(db.Model):
    
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    #categoryproducts = db.relationship('Category', backref='products', lazy='select')
    
    def __init__(self, name, price, id, category_id):
        self.id = id
        self.name = name
        self.price = price
        self.category_id=category_id
        
    def __repr__(self):
        return '<Product %d>' % (self.id)

class ProductForm(FlaskForm):
    name = StringField("Nombre", validators=[InputRequired()])
    price = DecimalField('Precio', validators=[InputRequired(),NumberRange(min=Decimal('0.0'))])
    Id = DecimalField('Id')
    category_id = SelectField('Categoría', coerce=int)
    