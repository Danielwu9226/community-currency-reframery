from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:newpassword@localhost/reframery'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import enum
class Category(enum.Enum):
    PRODUCT = "product"
    SERVICE = "service"
    EXPERTISE = "expertise"

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    address = db.relationship('Address')
    email = db.Column(db.String())
    username = db.Column(db.String())
    phone_number = db.Column(db.String())
    community_id = db.Column(db.String())
    is_admin = db.Column(db.Boolean, default = False)
    registerTime = db.Column(db.DateTime, default = datetime.utcnow())
    birthday = db.Column(db.DateTime)
    user_image = db.Column(db.String())
    validate_status = db.Column(db.Boolean)
    
class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key = True)
    address_line_1 = db.Column(db.String())
    address_line_2 = db.Column(db.String())
    city = db.Column(db.String())
    country = db.Column(db.String())
    postal_code = db.Column(db.String())
    
class Community(db.Model):
    __tablename__ = 'community'
    id = db.Column(db.Integer, primary_key = True)
    name: db.Column(db.String())

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.Enum(Category))
    name = db.Column(db.String())
    image = db.Column(db.String())
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    description = db.Column(db.String())
    discount = db.Column(db.Float)
    user_id = db.relationship('User')
    
class SubCategory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    user_id = db.relationship('User')

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.relationship('User')
    item_id = db.relationship('Item')
    rating = db.Column(db.Integer)
    created_time = db.Column(db.DateTime, default = datetime.utcnow())
    description = db.Column(db.String())
    

class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key = True)
    sender_id = db.relationship('User')
    receiver_id = db.relationship('User')
    time = db.Column(db.DateTime, default = datetime.utcnow())
    amount = db.Column(db.Integer)
    txid = db.Column(db.String())
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item_id = db.relationship('Item')
    buyer_id = db.relationship('User')
    seller_id = db.relationship('User')
    quantity = db.Column(db.Integer)
    status = db.Column(db.String())
    txid = db.relationship('Transaction')
    
    
@app.route('/')
def main():
    return "Cryptocurrency Reframery Project"

if __name__ == '__main__':
    app.run()