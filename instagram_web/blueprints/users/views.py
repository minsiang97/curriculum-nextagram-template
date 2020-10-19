from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from models.user import User
from flask_login import login_required, current_user, login_user



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
        signed_in = True
        flash("Successfully Logged In!","success")
        return render_template('home.html',signed_in=signed_in)
    else :
        flash(user.errors,"danger")
    return redirect(url_for('users.new'))
    
    


@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    username = User.get(User.username == username)
    return render_template('users/show.html',name=current_user.name)



@users_blueprint.route('/', methods=["GET"])
def index():

    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
