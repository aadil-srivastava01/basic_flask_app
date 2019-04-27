from flask import request
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Stores(Resource):

    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type = str,
                        required = True,
                        help = 'This field canot be left blank')

    def get(self,name):

        store = StoreModel.find_by_name(name)

        if store:
            return store.json(),200
        else:
            return {"Message":"Store Not found"} ,404

    @jwt_required()
    def post(self,name):

        store = StoreModel.find_by_name(name)

        if store:
            return {"Message": "Store already present"},400
        else:
            try:
                store = StoreModel(name)
                store.save_to_db()
                return {"Message","Store Created"},201
            except:
                return{"Message","Error occured"},500

    @jwt_required()
    def delete(self,name):

        store = StoreModel.find_by_name(name)

        if store:

            store = StoreModel(name)
            store.delete_from_db()
            return {"Message","Store Deleted"},201

        else:

            return {"Message": "Store Not found"},400
