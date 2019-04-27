from flask_restful import Resource,reqparse
from models.myuser import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True,
                        help = 'Field cannot be left blank')
    parser.add_argument('password',type=str,required=True,
                        help = 'Field cannot be left blank')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"Message": "Username already present"},400

        user = UserModel(**data)
        user.save_to_db()
        return {"Message":f"{user.username} sucessfully created!"},201
