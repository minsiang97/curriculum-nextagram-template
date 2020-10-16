from models.base_model import BaseModel
import peewee as pw
import re


class User(BaseModel):
    name = pw.CharField(unique=False)
    username = pw.CharField(unique=True, null=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=False)


    def validate(self):
        duplicate_user_email = User.get_or_none(User.email == self.email)
        duplicate_user_username = User.get_or_none(User.username == self.username)

        if duplicate_user_email or duplicate_user_username:
            self.errors.append('User email or username not unique')
    
    
        
        
        
  

        

        