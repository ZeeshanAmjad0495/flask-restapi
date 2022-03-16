from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, timedelta

from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.secret_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDc0MjA1ODMsImlhdCI6MTY0NzQyMDI4MywibmJmIjoxNjQ3NDIwMjgzLCJpZGVudGl0eSI6MX0.bsuz5_smQap27_BjAMuvFYlBxU2kaTp4eojCmSQJHTg'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'access_token': 'JWT ' + access_token.decode('utf-8'),
        'user_id': identity.id
    })


@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
        'message': error.description,
        'code': error.status_code
    }), error.status_code


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
