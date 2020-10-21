from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from playhouse.hybrid import hybrid_property
from flask_login import UserMixin


class User(BaseModel,UserMixin):
    name = pw.CharField(unique=False)
    username = pw.CharField(unique=True, null=True)
    email = pw.CharField(unique=True)
    password_hash = pw.CharField(unique=False)
    image_path = pw.CharField(null = True)
    is_private = pw.BooleanField(default = False)
    password = None

    
    

    def validate(self):
        duplicate_user_email = User.get_or_none(User.email == self.email)
        duplicate_user_username = User.get_or_none(User.username == self.username)

        if duplicate_user_email and self.id != duplicate_user_email.id:
            self.errors.append('Email already exist')
        
        if duplicate_user_username and self.id != duplicate_user_username.id:
            self.errors.append('Username already exist')

        if self.password:
            if len(self.password) < 6:
                self.errors.append("Password must be at least 6 characters")
            if not re.search("[a-z]", self.password):
                self.errors.append("Password must be include lowercase")
            if not re.search("[A-Z]", self.password):
                self.errors.append("Password must be include uppercase")
            if not re.search("[\](\)!^%$&*#@]", self.password):
                self.errors.append("Password must be include special characters")
        
            if len(self.errors)==0:
                self.password_hash = generate_password_hash(self.password)
        
        if not self.password_hash:
            self.errors.append("Password must be present")


    def is_active(self):
        
        return True

    def get_id(self):
        
        return self.id

    def is_authenticated(self):
        
        return self.authenticated

    def is_anonymous(self):
        
        return False
    
    
        
    @hybrid_property
    def profile_image_url(self):
        from app import app
        if not self.image_path :
            return app.config.get("AWS_S3_DOMAIN") + "avatar.png"
        return app.config.get("AWS_S3_DOMAIN") + self.image_path
        
  

        

        