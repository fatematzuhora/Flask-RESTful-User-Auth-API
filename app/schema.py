from app import app

from app.models import User
from flask_marshmallow import Marshmallow


ma = Marshmallow(app)


"""
=============
schema classes
=============
"""

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        fields = ('uuid', 'username', 'mobile', 'status') # fields to expose


user_schema = UserSchema()
users_schema = UserSchema(many=True)