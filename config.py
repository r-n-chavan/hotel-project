from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manytone.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:root@localhost/restdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '1238sadh1234390823kjhdJKA*(@E$^$'
