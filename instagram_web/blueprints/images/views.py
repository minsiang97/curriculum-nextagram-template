from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from models.image import Image
from flask_login import login_required, current_user, login_user
from models.user import User
from helpers import upload_file_to_s3

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/new', methods=['GET'])
def new():
    user = User.get_or_none(User.id == current_user.id)
    image = Image.select(Image, User).join(User).where(Image.user_id == user.id)
    return render_template('images/new.html', user =user, image = image)


@images_blueprint.route('/', methods=['POST'])
def create():
    user = User.get_or_none(User.id == current_user.id)
    
    if user :
        if "image_file" not in request.files:
            return "No image_file key in request.files"

	
        file = request.files["image_file"]



        if file.filename == "":
            return "Please select a file"

	
        if file :
            file_path = upload_file_to_s3(file)
            image = Image(user = user, image_url= file_path)

            if image.save() :
                flash("Image uploaded successfully","success")
                return redirect(url_for('users.show',username = current_user.username))
            else :
                flash("Failed to upload images, try again","danger")
                return redirect(url_for('images.new'))

        else:
            return redirect(url_for('images.new'))
    else :
        return "No such user found!"
    
    
    
