from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from werkzeug.security import check_password_hash

sessions_api_blueprint = Blueprint('sessions_api',
                             __name__,
                             template_folder='templates')

@sessions_api_blueprint.route('/login', methods=['POST'])
def login():
    email = request.json.get('user_email')
    user = User.get_or_none(User.email == email)
    if user :
        password_to_check = request.json.get('user_password')
        hashed_password = user.password_hash
        result = check_password_hash(hashed_password, password_to_check)
        if result:
            token = create_access_token(identity = user.id)
            return jsonify ({"token" : token})
    
    return jsonify ({"Error" : "Invalid Credentials"})