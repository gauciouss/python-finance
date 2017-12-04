from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column,String, Float, Date, Integer
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Server
import pymysql


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://finance:12345678@192.168.174.140/finance"
db = SQLAlchemy(app)

def db_init():
    db.create_all()

class StkCompInfo(db.Model):
    __tablename__ = "stk_comp_info"
    stk_id = db.Column(String(10), primary_key=True)
    comp_name = db.Column(String(100))
    isin_code = db.Column(String(30))
    marketing_date = db.Column(Date)
    industry_class = db.Column(Integer)
    market = db.Column(Integer)

    def __repr__(self):
        return "<stk_comp_info: stk_id: {}, comp_name: {}>".format(self.stk_id, self.comp_name)



comp = StkCompInfo.query.filter_by(stk_id = "2330").first()
print(comp)