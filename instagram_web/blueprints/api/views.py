from flask import Blueprint, render_template, flash, request, redirect, url_for, session, jsonify
from flask_login import login_required, current_user, login_user
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt_claims

api_blueprint = Blueprint('api',
                            __name__,
                            template_folder='templates')

@api_blueprint.route('/create_token')
def create():
    return jsonify(create_access_token(identity="user_id"))

@api_blueprint.route('/receive_token')
@jwt_required
def receive():
    identity = get_jwt_identity()
    return(identity)

