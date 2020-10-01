import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from resources.db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = User(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201




class UserAccounts(Resource):
    TABLE_NAME = 'users'

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self):
        connection = sqlite3.connect('./data/data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        usernames = []
        for row in result:
            usernames.append({'username': row[1]})
        connection.close()

        return {'usernames': usernames}

    @jwt_required()
    def delete(self):
        data = UserAccounts.parser.parse_args()
        User.query.filter_by(username=data['username']).delete()

        return {'message': 'User has now been deleted from the database'}
