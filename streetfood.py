from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from bs4 import BeautifulSoup
from selenium import webdriver

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
    return 'FOod khaalo'

class street_food(db.Model):
    rId=db.Column(db.Integer, primary_key=True)
    rName=db.Column(db.String(10), nullable=False)
    rLat= db.Column(db.Float, nullable=False)
    rLong= db.Column(db.Float, nullable=False)
    rAddress=db.Column(db.String(50), nullable=False)
    rCost=db.Column(db.Integer)
    rRating=db.Column(db.Float)
    rItems=db.Column(db.String(100))
    rUrl=db.Column(db.String(50))

    def __init__(self,rName,rLat,rLong,rAddress,rCost,rRating,rItems,rUrl):
        self.rName=rName
        self.rLat=rLat
        self.rLong=rLong
        self.rAddress=rAddress
        self.rCost=rCost
        self.rRating=rRating
        self.rItems=rItems
        self.rUrl=rUrl

class StreetFoodSchema(ma.Schema):
    class Meta:
        fields=('rId','rName','rLat','rLong','rAddress','rCost','rRating','rItems','rUrl')

streetFood_schema=StreetFoodSchema()
streetFoods_schema=StreetFoodSchema(many=True)


@app.route('/food')
def homepage():
    params = {'user-key': 'b4072fa4fc94bd77ebd31709d42ae167'}
    cnt=0
    r = requests.get('https://developers.zomato.com/api/v2.1/search?entity_id=5&entity_type=city&start={}&cuisines=55&sort=cost&order=asc'.format(cnt),headers=params)
    obj=r.json()
    total=obj["results_found"]

    for i in range(0,min(100,total)):
        if(i!=0 and i%20==0):
            cnt=cnt+20
            r = requests.get('https://developers.zomato.com/api/v2.1/search?entity_id=5&entity_type=city&start={}&cuisines=55&sort=cost&order=asc'.format(cnt),headers=params)
            obj=r.json()
        name=obj["restaurants"][i-cnt]["restaurant"]["name"]
        url=obj["restaurants"][i-cnt]["restaurant"]["url"]
        cost=obj["restaurants"][i-cnt]["restaurant"]["average_cost_for_two"]
        rating=obj["restaurants"][i-cnt]["restaurant"]["user_rating"]["aggregate_rating"]
        address=obj["restaurants"][i-cnt]["restaurant"]["location"]["address"]
        lat=obj["restaurants"][i-cnt]["restaurant"]["location"]["latitude"]
        lng=obj["restaurants"][i-cnt]["restaurant"]["location"]["longitude"]
        browser = webdriver.Firefox()
        browser.get(url)
        html_text = browser.page_source
        soup = BeautifulSoup(html_text, 'lxml')
        st=""
        if(soup.find('div',class_='fontsize13')):
            l=soup.find('div',class_='fontsize13').text.split()
            for i in l:
                st=st+i
        items=st
        browser.close()
        new_food=Italian(name,lat,lng,address,cost,rating,items,url)
        db.session.add(new_food)
        db.session.commit()
    return "Add ho gaya sb"

@app.route("/api/streetfoods", methods=["GET"])
def get_street_food():
    all_products= street_food.query.all()
    result= streetFoods_schema.dump(all_products)
    return jsonify(result.data)

if __name__ == "__main__":
    app.run(debug=True)
