from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash


class User(BaseModel):
    name = pw.CharField(unique=False)
    username = pw.CharField(unique=True, null=True)
    email = pw.CharField(unique=True)
    password_hash = pw.CharField(unique=False)
    password = None


    def validate(self):
        duplicate_user_email = User.get_or_none(User.email == self.email)
        duplicate_user_username = User.get_or_none(User.username == self.username)

        if duplicate_user_email:
            self.errors.append('Email already exist')
        
        if duplicate_user_username:
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
        
        if not self.password:
            self.errors.append("Password must be present")



    
    
        
        
        
  

        

        