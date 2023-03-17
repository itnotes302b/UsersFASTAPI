from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50)
    docname = fields.CharField(max_length=50)
    dateofappoint = fields.DateField(auto_now_add=False)
    # password_hash = fields.CharField(max_length=128 , null=False)

User_Pydantic = pydantic_model_creator(User,name='User')
UserIn_Pydantic = pydantic_model_creator(User,name="UserIn", exclude_readonly=True)
