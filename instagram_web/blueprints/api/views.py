from flask import Blueprint, render_template, flash, request, redirect, url_for, session, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt_claims

api_blueprint = Blueprint('api',
                            __name__,
                            template_folder='templates')

@api_blueprint.route('/create_token', methods=['POST'])
def create():
    access_token = create_access_token(identity=current_user.id)
    ret = {'access_token': access_token}
    return jsonify (ret)
