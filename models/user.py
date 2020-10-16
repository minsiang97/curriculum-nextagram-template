from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name = pw.CharField(unique=False)
    username = pw.CharField(unique=True, null=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=False)


    def validate(self):
        duplicate_user_email = User.get_or_none(User.email == self.email)

        if duplicate_user_email:
            self.errors.append('User email not unique')