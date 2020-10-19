from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user



sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    email = request.form.get('user_email')
    user = User.get(User.email == email)
    password_to_check = request.form['user_password']
    hashed_password = user.password_hash
    result = check_password_hash(hashed_password, password_to_check)
    
    
    if result == True:
        session["user_id"] = user.id
        login_user(user)
        signed_in = True
        flash("Successfully Logged In!","success")
        return render_template('home.html',signed_in=signed_in)
        
    else :
        flash("Email or password is incorrect","danger")
    return redirect(url_for('sessions.new'))
    
@sessions_blueprint.route("/logout")
def logout():
    session.pop('user_id', None)
    flash("Successfully Logged Out!", "success")
    return redirect(url_for('home'))
    


