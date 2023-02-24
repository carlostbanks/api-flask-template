from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS, cross_origin
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


api = Blueprint('api', __name__)
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = jsonify(message='Simple server is running')
    response_body.headers.add('Access-Control-Allow-Origin', '*')
    return response_body, 200




# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.


@api.route('/login', methods=['POST'])
@cross_origin()
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'message': 'Invalid data'}), 400

    user = User.query.filter_by(email=email,password=password).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

   
    token= create_access_token(identity=user.id)
    return jsonify({
        "message": "successfully logged in",
        "token": token
    }),200



@api.route('/signup', methods=['POST'])
@cross_origin()
def signup():

    email = request.json.get('email', None)
    name = request.json.get('name', None)
    password = request.json.get('password', None)
    
    if not email:
        return "email is required", 401
    if not name:
        return "name is required", 401 
    if not password:
        return "password is required", 401   

    email_check= User.query.filter_by(email=email).first() 
    if email_check: 
        return "this email already exist",401


    user = User(email=email, name=name, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', "email": email})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response 


