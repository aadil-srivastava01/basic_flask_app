from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.myitems import ItemModel

class Items(Resource):

    def get(self):

        return {"items": [item.json() for item in ItemModel.query.all()]}


class Item(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('price',
                type=float,
                required=True,
                help = 'This field canot be left blank')
    parser.add_argument('store_id',
                type=int,
                required=True,
                help = 'This field canot be left blank')

    def get(self,name):

        item = ItemModel.find_by_name(name)
        if item:
            return item.json(),200
        return {"message":"Item not found"},404

    @jwt_required()
    def post(self,name):

        item = ItemModel.find_by_name(name)
        if item:
            return {"Message":f"{item.name} already exists"},400

        data = Item.parser.parse_args()

        try:
            item = ItemModel(name,**data)
            item.save_to_db()
        except:
            return{"Message": "Item Not Inserted"},500

        return {"Message":item.json()},201

    @jwt_required()
    def delete(self,name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"Message":"Item Deleted"}

    @jwt_required()
    def put(self,name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name,**data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json(),201
