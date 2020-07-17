import traceback
from app import app, db

from app.models import User
from app.schema import user_schema, users_schema

from flask import request, jsonify, make_response
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)

from config import Config
import hashlib
from blacklist import BLACKLIST


# method to generate hash_password
def hash_password(string):
    salt = Config.SALT_KEY
    hash_key = string + salt

    hash_password = hashlib.md5(hash_key.encode()).hexdigest()

    return hash_password


# return messages
USER_ALREADY_EXISTS = "A user with that username already exists."
MOBILE_ALREADY_EXISTS = "A user with that mobile number already exists."
EMAIL_ALREADY_EXISTS = "A user with that email already exists."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
UNAUTHORIZED_ACCESS = "Unauthorized access!"
USER_LOGGED_OUT = "User {} successfully logged out."
NOT_CONFIRMED_ERROR = "Your account have not confirmed yet!"
FAILED_TO_CREATE = "Internal server error. Failed to create user."
FAILED_TO_ACCESS = "Internal server error. Unable to get data."
SUCCESS_REGISTER_MESSAGE = "Account created successfully!"
SUCCESS_MESSAGE = "Success!"

"""
================================
endpoints for USER AUTH and CRUD
================================
"""

# endpoint to CREATE new user OR registration
@app.route("/user", methods=["POST"])
def user_registration():
    username = request.json['username']
    mobile = request.json['mobile']
    entered_password = request.json['password']

    if User.find_by_username(username):
        return {'message': USER_ALREADY_EXISTS}, 400
    if User.find_by_mobile(mobile):
        return {'message': MOBILE_ALREADY_EXISTS}, 400

    try:
        db_password = hash_password(entered_password)
        new_user = User(username, mobile, db_password)
        User.save(new_user)

        result = user_schema.dump(new_user)

        data = {
            'message': SUCCESS_REGISTER_MESSAGE,
            'status': 201,
            'data': result
        }
        return make_response(jsonify(data))
    except:
        traceback.print_exc()
        return {'message': FAILED_TO_CREATE}, 500


# endpoint to LOGIN
@app.route("/user/login", methods=["POST"])
def user_login():
    username = request.json['username']
    entered_password = request.json['password']

    user = User.find_by_username(username)

    if user:
        password = hash_password(entered_password)

        if user and safe_str_cmp(password, user.password):
            if user.status:
                try:
                    access_token = create_access_token(identity=user.uuid, fresh=True)
                    refresh_token = create_refresh_token(user.uuid)

                    data = {
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }
                    return make_response(jsonify(data))
                except:
                    traceback.print_exc()
                    return {'message': FAILED_TO_ACCESS}, 500

            return {'message': NOT_CONFIRMED_ERROR}, 400

        return {'message': INVALID_CREDENTIALS}, 401
        
    return {'message': USER_NOT_FOUND}, 404


# endpoint to CHANGE_PASSWORD
@app.route("/user/change-password/<path:uuid>", methods=["POST"])
@jwt_required
def change_password(uuid):
    current_user = get_jwt_identity()
    if current_user:
        user = User.find_by_id(uuid)

        if user:
            try:
                old_password = request.json['old_password']
                new_password = request.json['new_password']

                old_db_password = hash_password(old_password)
                
                if user and safe_str_cmp(old_db_password, user.password):
                    new_db_password = hash_password(new_password)
                    user.password = new_db_password
                    User.save(user)
                    return {'message': SUCCESS_MESSAGE}, 200
                
                return {'message': INVALID_CREDENTIALS}, 401
            except:
                traceback.print_exc()
                return {'message': FAILED_TO_ACCESS}, 500
        
        return {'message': USER_NOT_FOUND}, 404

    return {'message': UNAUTHORIZED_ACCESS}, 401


# endpoint to GET all users
@app.route("/user", methods=["GET"])
@jwt_required
def get_users():
    current_user = get_jwt_identity()
    if current_user:
        try:
            all_users = User.query.all()
            result = users_schema.dump(all_users)

            data = {
                'message': SUCCESS_MESSAGE,
                'status': 200,
                'data': result
            }
            return make_response(jsonify(data))
        except:
            traceback.print_exc()
            return {'message': FAILED_TO_ACCESS}, 500

    return {'message': UNAUTHORIZED_ACCESS}, 401


# endpoint to GET user detail by uuid
@app.route("/user/<path:uuid>", methods=["GET"])
@jwt_required
def user_detail(uuid):
    current_user = get_jwt_identity()
    if current_user:
        user = User.find_by_id(uuid)

        if user:
            try:
                result = user_schema.dump(user)
                data = {
                    'message': SUCCESS_MESSAGE,
                    'status': 200,
                    'data': result
                }
                return make_response(jsonify(data))
            except:
                traceback.print_exc()
                return {'message': FAILED_TO_ACCESS}, 500

        return {'message': USER_NOT_FOUND}, 404

    return {'message': UNAUTHORIZED_ACCESS}, 401


# endpoint to UPDATE user
@app.route("/user/<path:uuid>", methods=["PATCH"])
@jwt_required
def update_user(uuid):
    current_user = get_jwt_identity()
    if current_user:
        user = User.find_by_id(uuid)

        if user:
            try:
                if 'username' in request.json:
                    if User.find_by_username(request.json['username']):
                        return {'message': USER_ALREADY_EXISTS}, 400
                    user.username = request.json['username']

                if 'email' in request.json:
                    if User.find_by_username(request.json['email']):
                        return {'message': EMAIL_ALREADY_EXISTS}, 400
                    user.email = request.json['email']

                if 'mobile' in request.json:
                    if User.find_by_username(request.json['mobile']):
                        return {'message': MOBILE_ALREADY_EXISTS}, 400
                    user.mobile = request.json['mobile']

                if 'gender' in request.json:
                    user.gender = request.json['gender']

                User.save(user)
                result = user_schema.dump(user)
                
                data = {
                    'message': SUCCESS_MESSAGE,
                    'status': 200,
                    'data': result
                }
                return make_response(jsonify(data))

            except:
                traceback.print_exc()
                return {'message': FAILED_TO_ACCESS}, 500

        return {'message': USER_NOT_FOUND}, 404

    return {'message': UNAUTHORIZED_ACCESS}, 401


# endpoint to DELETE user
@app.route("/user/<path:uuid>", methods=["DELETE"])
@jwt_required
def delete_user(uuid):
    current_user = get_jwt_identity()
    if current_user:
        user = User.find_by_id(uuid)

        if user:
            try:
                User.delete(user)
                data = {
                    'message': USER_DELETED,
                    'status': 200
                }
                return make_response(jsonify(data))
            except:
                traceback.print_exc()
                return {'message': FAILED_TO_ACCESS}, 500

        return {'message': USER_NOT_FOUND}, 404

    return {'message': UNAUTHORIZED_ACCESS}, 401


# endpoint to ACTIVATE user account
@app.route("/user/activate-account/", methods=["POST"])
def activate_account():
    if 'mobile' in request.json:
        user = User.find_by_mobile(request.json['mobile'])
        if user:
            try:
                user.status = True
                User.save(user)
                result = user_schema.dump(user)

                data = {
                    'message': SUCCESS_MESSAGE,
                    'status': 200,
                    'data': result
                }
                return make_response(jsonify(data))
            except:
                traceback.print_exc()
                return {'message': FAILED_TO_ACCESS}, 500

        return {'message': USER_NOT_FOUND}, 404


# endpoint to REFRESH_TOKEN
@app.route("/user/refresh-token/", methods=["GET"])
@jwt_refresh_token_required
def refresh_token():
    current_user = get_jwt_identity()
    if current_user:
        try:
            new_token = create_access_token(identity=current_user, fresh=False)
            return {'access_token': new_token}, 200
        except:
            traceback.print_exc()
            return {'message': FAILED_TO_ACCESS}, 500

    return {'message': UNAUTHORIZED_ACCESS}, 401


# endpoint to LOGOUT
@app.route("/user/logout/", methods=["GET"])
@jwt_required
def logout():
    jti = get_raw_jwt()["jti"]
    current_user = get_jwt_identity()
    if current_user:
        try:
            user = User.find_by_id(current_user)
            BLACKLIST.add(jti)
            return {'message': USER_LOGGED_OUT.format(user.username)}, 200
        except:
            traceback.print_exc()
            return {'message': FAILED_TO_ACCESS}, 500

    return {'message': UNAUTHORIZED_ACCESS}, 401