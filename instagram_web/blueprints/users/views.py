from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from models.user import User
from flask_login import login_required, current_user, login_user
from helpers import *
from config import ProductionConfig



users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    name = request.form.get('user_name')
    username = request.form.get('user_username')
    email = request.form.get('user_email')
    password = request.form.get('user_password')
    user = User(name=name, username = username, email = email, password = password)
    if user.save():
        session["user_id"] = user.id
        login_user(user)
        flash("Successfully Logged In!","success")
        return redirect(url_for('home'))
    else :
        flash(user.errors,"danger")
    return redirect(url_for('users.new'))
    
    


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get(User.username == username)
    return render_template('users/show.html',name=user.name)



@users_blueprint.route('/', methods=["GET"])
def index():

    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_by_id(id)
    if current_user == user:
        return render_template('users/edit.html')
    else :
        return redirect(url_for('users.show', username = user.username))



@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_by_id(id)
    user.username = request.form.get('user_username')
    user.email = request.form.get('user_email')
    user.password = request.form.get('user_password')
    
    if user.save() :
        flash("Successfully Updated","success")
        return redirect(url_for('users.show',username = current_user.username))
    else :
        flash("Update failed, try again.","danger")
    return redirect(url_for('users.edit',id = current_user.id))


@users_blueprint.route('/<id>', methods=['POST'])
def upload_image(id) :
    user = User.get_by_id(id)
    if "user_file" not in request.files:
        return "No user_file key in request.files"
    
    file    = request.files["user_file"]

    if file.filename == "":
        return "Please select a file"

    if file :
        output = upload_file_to_s3(file, ProductionConfig.S3_BUCKET)
        str(output)
        return redirect(url_for("users.show", username =current_user.username))
        

    else:
        return redirect(url_for("users.show", username =current_user.username))
    
  

