from my_app import db
from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import InputRequired, NumberRange

class Category(db.Model):
    
    __tablename__='categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    products = db.relationship('Product', backref='category', lazy='select')
    
    def __init__(self, name, id):
        self.id = id
        self.name = name
        
    def __repr__(self):
        return '<Category %d>' % (self.id)

class CategoryForm(FlaskForm):
    name = StringField("Nombre", validators=[InputRequired()])
    Id = DecimalField('Id')