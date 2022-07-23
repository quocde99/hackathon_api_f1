from time import time
from unicodedata import name
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime as dt


app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class Stock_symbol(db.Model):
    # __tablename__ = "stock_symbol"
    stock_symbol_id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    reason = db.Column(db.String(120), unique=False, nullable=False)
    is_fraud = db.Column(db.BOOLEAN, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, unique=False,
                           nullable=False)
    updated_at = db.Column(db.DateTime, unique=False,
                           nullable=False)

    def __init__(self, stock_symbol_id, name, reason, is_fraud, created_at, updated_at):
        self.stock_symbol_id = stock_symbol_id
        self.name = name
        self.reason = reason
        self.is_fraud = is_fraud
        self.created_at = created_at
        self.updated_at = updated_at


class User(db.Model):
    # __tablename__ = "user"
    username = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, username, name, created_at, updated_at):
        self.username = username
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at


class User_Stock(db.Model):
    __tablename__ = "user_stock"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('user.username'))
    stock_symbol_id = db.Column(
        db.String(20), foreign_keys='stock_symbol.stock_symbol_id')
    time_start = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(self, time_start, username, stock_symbol_id):
        self.time_start = time_start
        self.username = username
        self.stock_symbol_id = stock_symbol_id


db.create_all()

# add data and test
#data_u1 = User("HungND74", "HungND74", dt.now(), dt.now())
#data_u2 = User("DePQ", "DePQ", dt.now(), dt.now())
#symbol_1 = Stock_symbol("FPT", "FPT", "No", False, dt.now(), dt.now())
#symbol_2 = Stock_symbol("FLC", "FLC", "No", True, dt.now(), dt.now())
# User_Stock
# user_stock_1 = User_Stock(dt.now(),"DePQ", "FLC")
# user_stock_2 = User_Stock(dt.now(),"DePQ", "FPT")
#db.session.add(data_u1)
#db.session.add(data_u2)
#db.session.add(symbol_1)
#db.session.add(symbol_2)
# db.session.add(user_stock_1)
# db.session.add(user_stock_2)
# db.session.commit()


@app.route('/symbols/<stock_symbol_id>', methods=['GET'])
def get_item(stock_symbol_id):
    item = Stock_symbol.query.get(stock_symbol_id)
    del item.__dict__['_sa_instance_state']
    return jsonify(item.__dict__)


@app.route('/symbols', methods=['GET'])
def get_items():
    items = []
    for item in db.session.query(Stock_symbol).all():
        del item.__dict__['_sa_instance_state']
        items.append(item.__dict__)
    return jsonify(items)


@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    item = User.query.get(username)
    del item.__dict__['_sa_instance_state']
    return jsonify(item.__dict__)


@app.route('/users', methods=['GET'])
def get_users():
    items = []
    for item in db.session.query(User).all():
        del item.__dict__['_sa_instance_state']
        items.append(item.__dict__)
    return jsonify(items)

@app.route('/list_intersted/<username>', methods=['GET'])
def get_list_intersted(username):
    items = []
    for item in User_Stock.query.filter_by(username=username).all():
        del item.__dict__['_sa_instance_state']
        items.append(item.__dict__)
    return jsonify(items)
