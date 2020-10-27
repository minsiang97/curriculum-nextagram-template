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
        
  
    
    def follow(self,idol):
        from models.fan_idol import FanIdol
        if self.follow_status(idol) == None:
            new_relationship = FanIdol(fan = self.id, idol = idol.id)
            if idol.is_private == False :
                new_relationship.is_approved = True
            return new_relationship.save()
        else :
            return 0

    def unfollow(self,idol):
        from models.fan_idol import FanIdol
        return FanIdol.delete().where(FanIdol.idol ==idol.id, FanIdol.fan==self.id).execute()

    def follow_status(self, idol):
        from models.fan_idol import FanIdol
        return FanIdol.get_or_none(fan = self.id, idol = idol.id)
    
    @hybrid_property
    def idols(self):
        from models.fan_idol import FanIdol
        idols_id = FanIdol.select(FanIdol.idol).where(FanIdol.fan == self.id, FanIdol.is_approved == True)
        idols = User.select().where(User.id.in_(idols_id))
        return idols

    @hybrid_property
    def fans(self):
        from models.fan_idol import FanIdol
        fans_id = FanIdol.select(FanIdol.fan).where(FanIdol.idol == self.id, FanIdol.is_approved == True)
        fans = User.select().where(User.id.in_(fans_id))
        return fans
    
    @hybrid_property
    def idol_requests(self):
        from models.fan_idol import FanIdol
        idols_id = FanIdol.select(FanIdol.idol).where(FanIdol.fan == self.id, FanIdol.is_approved == False)
        return User.select().where(User.id.in_(idols_id)).order_by(User.created_at.desc())
    
    @hybrid_property
    def fan_requests(self):
        from models.fan_idol import FanIdol
        fans_id = FanIdol.select(FanIdol.fan).where(FanIdol.idol == self.id, FanIdol.is_approved == False)
        return User.select().where(User.id.in_(fans_id)).order_by(User.created_at.desc())
    
    def approve(self, fan):
        from models.fan_idol import FanIdol
        relationship = FanIdol.get_or_none(idol=self.id, fan=fan.id)
        relationship.is_approved = True
        return relationship.save()

    @hybrid_property
    def image_feed(self):
        from models.fan_idol import FanIdol
        from models.image import Image
        approved_idols_id = FanIdol.select(FanIdol.idol).where(FanIdol.fan == self.id, FanIdol.is_approved == True)
        return Image.select().where(Image.user.in_(approved_idols_id)).order_by(Image.created_at.desc())       