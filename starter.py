from flask import Flask
import pymysql
import db_secrets
from flask_sqlalchemy import SQLAlchemy

# * ---------- Create App --------- *
app = Flask(__name__)
app.secret_key = "64yuuryurei984748wsifddi8"
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(db_secrets.dbuser,db_secrets.dbpass,db_secrets.dbhost,db_secrets.dbname)
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db =  SQLAlchemy(app)
