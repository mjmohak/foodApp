from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from northIndian import get_north_indian
from southIndian import get_south_indian
from streetfood import get_street_food
from chinese import get_chinese
from desert import get_deserts
import requests
import os

app=Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir, 'pune.sqlite')
db=SQLAlchemy(app)
ma=Marshmallow(app)

@app.route('/')
def home():
    return 'API Services Online'

@app.route("/api/streetfoods", methods=["GET"])
def GetStreetFood():
    return get_street_food()

@app.route("/api/deserts", methods=["GET"])
def GetDeserts():
    return get_deserts()

@app.route("/api/chinese", methods=["GET"])
def GetChineses():
    return get_chinese()

@app.route("/api/southindian", methods=["GET"])
def GetSouthIndians():
    return get_south_indian()

@app.route("/api/northindian", methods=["GET"])
def GetNorthIndians():
    return get_north_indian()

if __name__ == "__main__":
    app.run(debug=True)
