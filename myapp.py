from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from mysecurity import authenticate, identity
from resources.myuser import UserRegister
from resources.myitems import Items,Item
from resources.store import Store,Stores

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '#@$%1707@@#$1995'
api = Api(app)

jwt = JWT(app,authenticate,identity) #/auth

#http:/127.0.0.1:5000/item/<name>
api.add_resource(Item,'/item/<string:name>')
api.add_resource(Items,'/items')
api.add_resource(UserRegister,'/signup')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(Stores,'/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug = True)
