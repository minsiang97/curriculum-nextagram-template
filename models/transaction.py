from models.base_model import BaseModel
from models.user import User 
from models.image import Image 
import peewee as pw


class Transaction(BaseModel):
    image = pw.ForeignKeyField(Image, backref = "donations", on_delete = "CASCADE")
    user = pw.ForeignKeyField(User, backref = "donations", on_delete = "CASCADE")
    donation_amount = pw.DecimalField(decimal_places = 2)







