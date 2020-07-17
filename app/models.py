from app import db

from uuid import uuid4
import datetime


# method to generate uuid
def generate_uuid():
    return str(uuid4())


"""
=============
model classes
=============
"""
# See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
# for details on the column types.

class User(db.Model):
    __tablename__ = "users"

    uuid = db.Column(db.String(255), nullable=False, unique=True, default=generate_uuid, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    mobile = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10))
    status = db.Column(db.Boolean(), nullable=False, default=False)
    
    created = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), nullable=False)
    modified = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)


    def __init__(self, username, mobile, password):
        self.username = username
        self.mobile = mobile
        self.password = password

    @classmethod
    def find_by_id(cls, _id:str) -> "User":
        return cls.query.filter_by(uuid = _id).first()
    
    @classmethod
    def find_by_username(cls, _username:str) -> "User":
        return cls.query.filter_by(username = _username).first()
    
    @classmethod
    def find_by_mobile(cls, _mobile:str) -> "User":
        return cls.query.filter_by(mobile = _mobile).first()
    
    @classmethod
    def find_by_email(cls, _email:str) -> "User":
        return cls.query.filter_by(email = _email).first()
    
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()