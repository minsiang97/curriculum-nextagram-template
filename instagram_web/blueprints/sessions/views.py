from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from helpers import oauth



sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    email = request.form.get('user_email')
    user = User.get_or_none(User.email == email)
    password_to_check = request.form['user_password']
    
    if user :
        hashed_password = user.password_hash
        result = check_password_hash(hashed_password, password_to_check)
        if result:
            session["user_id"] = user.id
            login_user(user)
            flash("Successfully Logged In!","success")
            return redirect(url_for('home'))
        
        else:
            flash("Password is incorrect","danger")
            return redirect(url_for('sessions.new'))
    
    else :
        flash("Email does not exist","danger")
        return redirect(url_for('sessions.new'))
    
    
@sessions_blueprint.route("/logout")
def logout():
    logout_user()
    flash("Successfully Logged Out!", "success")
    return redirect(url_for('home'))
    


@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        return redirect(url_for('home'))
    else:
        flash("No such user with this email, please sign up an account with this email first!", "danger")
        return redirect(url_for('sessions.new'))