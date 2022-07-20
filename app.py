from time import time
from unicodedata import name
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class Stock_symbol(db.Model):
    stock_symbol_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    reason = db.Column(db.String(120), unique=True, nullable=False)
    is_fraud = db.Column(db.Bool, unique=True, nullable=False)

    def __init__(self, name, reason, is_fraud):
        self.name = name
        self.reason = reason
        self.is_fraud = is_fraud


class User(db.Model):
    username = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    time_start = db.Column(db.DATETIME, unique=False, nullable=False)
    time_end = db.Column(db.DATETIME, unique=False, nullable=True)
    stock_symbol_id = db.Column(db.String(20), unique=False, nullable=False)

    def __init__(self, name, time_start, time_end, stock_symbol_id):
        self.name = name
        self.time_start = time_start
        self.time_end = time_end
        self.stock_symbol_id = stock_symbol_id


db.create_all()

# symbol by time


@app.route('/symbol/<id>', methods=['GET'])
def get_item(id):
    item = Stock_symbol.query.get(id)
    del item.__dict__['_sa_instance_state']
    return jsonify(item.__dict__)


@app.route('/symbol', methods=['GET'])
def get_items():
    items = []
    for item in db.session.query(Stock_symbol).all():
        del item.__dict__['_sa_instance_state']
        items.append(item.__dict__)
    return jsonify(items)
