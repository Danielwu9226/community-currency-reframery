from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///reframery_project'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())

class Transaction(db.Model):
    __tablename__ = "transaction"
    
    id = db.Column(db.Integer, primary_key = True)
    txid = db.Column(db.String())

@app.route('/')
def main():
    return "Cryptocurrency Reframery Project"

if __name__ == '__main__':
    app.run()