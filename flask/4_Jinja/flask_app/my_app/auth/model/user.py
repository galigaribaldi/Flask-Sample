from my_app import db
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField,PasswordField,HiddenField
from wtforms.validators import EqualTo, InputRequired, NumberRange
from sqlalchemy import Enum
from werkzeug.security import check_password_hash, generate_password_hash
import enum

class RolUser(enum.Enum):
    regular = 'regular'
    admin = 'admin'

class User(db.Model):
    
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    pwhash = db.Column(db.String(300))
    rol = db.Column(Enum(RolUser))
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
    def __init__(self, username, pwhash, id,rol = RolUser.regular):
        self.id = id
        self.username = username
        self.pwhash = generate_password_hash(pwhash)
        self.rol = rol
        
    def __repr__(self):
        return '<User %r>' % (self.username)
    
    def check_password(self, password):
        return check_password_hash(self.pwhash, password)
    
class LoginForm(FlaskForm):
    name = StringField("Usuario", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    next = HiddenField("next")
    Id = DecimalField('Id')
    
class RegisterForm(FlaskForm):
    name = StringField("Usuario", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(),EqualTo('confirm')])
    confirm = PasswordField('Repeat Password')
    Id = DecimalField('Id')

class ChangePassword(FlaskForm):
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message="Confirma la contraseña")])
    confirm = PasswordField('Repeat Password')