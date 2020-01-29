from app import app, db

from app.models import User
from app.schema import user_schema, users_schema

from flask import request, jsonify, make_response

from config import Config
import hashlib



"""
===========================
endpoints for Category CRUD
===========================
"""

# endpoint to CREATE new user OR registration
@app.route("/user", methods=["POST"])
def user_registration():

    username = request.json['username']
    mobile = request.json['mobile']
    entered_password = request.json['password']

    salt = Config.SALT_KEY
    hash_password = entered_password + salt

    db_password = hashlib.md5(hash_password.encode()).hexdigest()
    
    new_user = User(username, mobile, db_password)

    db.session.add(new_user)
    db.session.commit()

    result = user_schema.dump(new_user)

    data = {
        'message': 'Success!',
        'status': 201,
        'data': result
    }
    return make_response(jsonify(data))



# endpoint to LOGIN
@app.route("/user/login", methods=["POST"])
def user_login(username, password):

    # user = User.query.where()



# endpoint to CHANGE_PASSWORD
@app.route("/user/change-password", methods=["POST"])
def change_password(username, old_password, new_password):

    # user = User.query.where()



# endpoint to GET all users
@app.route("/user", methods=["GET"])
def get_users():

    all_users = User.query.all()
    result = users_schema.dump(all_users)

    data = {
        'message': 'All Users!',
        'status': 200,
        'data': result
    }
    return make_response(jsonify(data))



# endpoint to GET user detail by uuid
@app.route("/user/<path:uuid>", methods=["GET"])
def user_detail(uuid):

    user = User.query.get(uuid)

    if(user):
        result = user_schema.dump(user)
        data = {
            'message': 'User Info!',
            'status': 200,
            'data': result
        }
    else:
        data = {
            'message': 'Invalid User ID!',
            'status': 200
        }
    return make_response(jsonify(data))



# endpoint to UPDATE user
@app.route("/user/<path:uuid>", methods=["PATCH"])
def update_user(uuid):

    user = User.query.get(uuid)

    if(user):
        if 'username' in request.json:
            user.username = request.json['username']
        if 'email' in request.json:
            user.email = request.json['email']
        if 'mobile' in request.json:
            user.mobile = request.json['mobile']
        if 'status' in request.json:
            user.status = request.json['status']
        
        db.session.commit()
        result = user_schema.dump(user)
        
        data = {
            'message': 'User Info Edited!',
            'status': 200,
            'data': result
        }

    else:
        data = {
            'message': 'Invalid User ID!',
            'status': 200
        }
    return make_response(jsonify(data))



# endpoint to DELETE user
@app.route("/user/<path:uuid>", methods=["DELETE"])
def delete_user(uuid):

    user = User.query.get(uuid)

    if(user):
        db.session.delete(user)
        db.session.commit()

        data = {
            'message': 'User Deleted!',
            'status': 200
        }
    else:
        data = {
            'message': 'Invalid User ID!',
            'status': 200
        }
    return make_response(jsonify(data))
