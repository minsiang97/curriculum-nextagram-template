from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from models.user import User
from models.image import Image
from flask_login import login_required, current_user, login_user
from helpers import upload_file_to_s3
from werkzeug.security import check_password_hash



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
    images = Image.select(Image, User).join(User).where(Image.user_id == user.id)
    return render_template('users/show.html',name=user.name, user = user, images = images )



@users_blueprint.route('/', methods=["GET"])
def index():

    return render_template("users/index.html")


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id == user.id:
            return render_template("users/edit.html", id = id, user = user)
        else :
            flash("You are not the owner of the account", "danger")
            return redirect(url_for('users.show', username = user.username))
    else :
        return "User does not exist"



@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_or_none(User.id == id)
    
    if user :
        if current_user.id == user.id:
            data = request.form
            hash_password = user.password_hash
            result = check_password_hash(hash_password, data.get('old_password'))
            if result :
                user.username = data.get("user_username")
                user.email = data.get("user_email")
                    
                if data.get("private") == "on":
                    user.is_private = data.get("private")

                if data.get("private") != "on" :
                    user.is_private = 0

                if data.get("user_password") != "":
                    user.password = data.get("user_password")                                                                                                                                    

                if user.save():
                    print(user.errors)
                    flash("Updated Successfully", "success")
                    return redirect(url_for('users.show', username = user.username))
                else :
                    return redirect(url_for('users.edit', id = user.id))
            else :
                flash ("Wrong Confirmation Password","danger")
                return redirect(url_for('users.edit', id = user.id)) 
        else :
            return "You are not the owner of the account!"

    else :
        return  "No such user found"               
    

@users_blueprint.route('/<id>/upload', methods=['POST'])
@login_required
def upload_image(id):
    user = User.get_or_none(User.id == current_user.id)
    if user :
        if "user_file" not in request.files:
            return "No user_file key in request.files"

	
        file = request.files["user_file"]



        if file.filename == "":
            return "Please select a file"

	
        if file :
            file_path = upload_file_to_s3(file)
            user.image_path = file_path
            if user.save() :
                return redirect(url_for('users.show',username = current_user.username))
            else :
                flash("Failed to upload images, try again","danger")
                return redirect(url_for('users.edit', id = current_user.id))

        else:
            return redirect(url_for('users.edit', id = current_user.id))
    else :
        return "No such user found!"

    
    
@users_blueprint.route('/search', methods=["POST"])
def search():
    user = User.select()
    if user:
        user.username = request.form.get("username")
        return redirect(url_for("users.show", username = user.username))
    else :
        return "User does not exist!"

