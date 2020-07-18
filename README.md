# Flask-RESTful-User-Auth-API
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg) [![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/fatematzuhora/Flask-RESTful-User-Auth-API)

A simple RESTful User Auth API built using [Flask](http://flask.pocoo.org) Framework & [SQLAlchemy](http://www.sqlalchemy.org), and connecting the both using [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org) library.

In this application, we are connecting a MySQL database in a python flask file in which there is ONE table named User. We use to add a new user / register a user, activate the user, login the user by authenticate using [JWT Token](https://flask-jwt-extended.readthedocs.io/), retrieve them. And later we can update and delete from the database.


## Getting started
* At first you'll need to get the source code of the project. Do this by cloning the [Flask-RESTful-User-Auth-API repository](https://github.com/fatematzuhora/Flask-RESTful-User-Auth-API).
```
$ git clone https://github.com/fatematzuhora/Flask-RESTful-User-Auth-API.git
$ cd Flask-RESTful-User-Auth-API
```

* Create a virtual environment for this project and install dependencies
```
$ virtualenv .venv
```

* Activate the virtual environment
```
$ source .venv/bin/activate
```

* Install the dependencies
```
$ pip install -r requirements.txt
```

* Create a environment file and configure it
```
$ touch .env
```

### Sample .env File
```
SECRET_KEY="w&8s%5^5vuhy2-gvkyi=gg4e*tso*51mb$l!=%o(@$a2tmq6o+Flask-RESTful-User-Auth-API"
DEBUG=TRUE
SQLALCHEMY_DATABASE_URI="mysql://YOUR_DB_USER_NAME:YOUR_DB_PASS@localhost:3306/YOUR_DB_NAME"
SQLALCHEMY_TRACK_MODIFICATIONS=FALSE
SALT_KEY="TEST_SALT_KEY"
```

* Update `SQLALCHEMY_DATABASE_URI` at the `.env` file according to your MySQL database information


## Running the App

#### 1) With Database Migration

```
$ export FLASK_APP=app.py
$ flask db init
```

* Create a migration file for all tables
```
$ flask db migrate -m tables
```

* Upgrade the database with migration file
```
$ flask db upgrade
```

* Run the app
```
$ flask run
```

And finally, the application will run on the following URL: http://127.0.0.1:5000

#### 2) Without Migration

* Simply run the following command, it will create database tables and run the project on the following URL: http://0.0.0.0:8087
* And the DEBUG mode will be ON

```
$ python app.py
```

If you want to change the PORT go to the [app.py](https://github.com/fatematzuhora/Flask-RESTful-User-Auth-API/blob/master/app.py) file and edit on the following line of code.
```
app.run(host='0.0.0.0', port=8087, debug=True)
```


## API Documentation

#### 1. User Registration

**Request**
```
POST /user
```

**Parameters**
Name|Type|Description
:-:|:-:|:-:
`username`|`string`|user name
`mobile`|`string`|user mobile number
`password`|`string`|user password

**Request Body**
```
{
    "username": "fatematzuhora",
    "mobile": "01XXXXXXXXX",
    "password": "password"
}
```

**Response**
```
{
    "data": {
        "mobile": "01XXXXXXXXX",
        "status": false,
        "username": "fatematzuhora",
        "uuid": "f99f6337-fde1-4f5c-990f-f3597b56770d"
    },
    "message": "Account created successfully!",
    "status": 201
}
```

#### 2. Activate User

**Request**
```
POST /user/activate-account/
```

**Parameters**
Name|Type|Description
:-:|:-:|:-:
`mobile`|`string`|user mobile number

**Request Body**
```
{
    "mobile": "01XXXXXXXXX"
}
```

**Response**
```
{
    "data": {
        "mobile": "01XXXXXXXXX",
        "status": true,
        "username": "fatematzuhora",
        "uuid": "f99f6337-fde1-4f5c-990f-f3597b56770d"
    },
    "message": "Success!",
    "status": 200
}
```

#### 3. User Login

**Request**
```
POST /user/login
```

**Parameters**
Name|Type|Description
:-:|:-:|:-:
`username`|`string`|user name
`password`|`string`|user password

**Request Body**
```
{
    "username": "fatematzuhora",
    "password": "password"
}
```

**Response**
```
{
    "access_token": "eyJ0eXAiOi....",
    "refresh_token": "eyJ0eXAiOi...."
}
```

#### 4. Token Refresh

**Request**
```
GET /user/refresh-token/
```

**Request Header**
```
'Authorization': 'Bearer THE_REFRESH_TOKEN'
```

**Response**
```
{
    "access_token": "eyJ0eXAiOi...."
}
```

#### 5. Logout

**Request**
```
GET /user/logout/
```

**Request Header**
```
'Authorization': 'Bearer THE_ACCESS_TOKEN'
```

**Response**
```
{
    "message": "User fatematzuhora successfully logged out."
}
```

#### 6. Get User Detail

**Request**
```
GET /user/:uuid
```

**Request Header**
```
'Authorization': 'Bearer THE_ACCESS_TOKEN'
```

**Response**
```
{
    "data": {
        "mobile": "01XXXXXXXXX",
        "status": true,
        "username": "fatematzuhora",
        "uuid": "f99f6337-fde1-4f5c-990f-f3597b56770d"
    },
    "message": "Success!",
    "status": 200
}
```

#### 7. Get User List

**Request**
```
GET /user
```

**Request Header**
```
'Authorization': 'Bearer THE_ACCESS_TOKEN'
```

**Response**
```
{
    "data": [
        {
            "mobile": "01XXXXXXXXX",
            "status": true,
            "username": "fatematzuhora",
            "uuid": "f99f6337-fde1-4f5c-990f-f3597b56770d"
        },
        ....
    ],
    "message": "Success!",
    "status": 200
}
```

#### 8. Update User

**Request**
```
PATCH /user/:uuid
```

**Request Header**
```
'Authorization': 'Bearer THE_ACCESS_TOKEN'
```

**Parameters**
Name|Type|Description
:-:|:-:|:-:
`username`|`string`|user name
`email`|`string`|user email address
`mobile`|`string`|user mobile number
`gender`|`string`|Male / Female

#### 9. Change Password

**Request**
```
POST /user/change-password/:uuid
```

**Request Header**
```
'Authorization': 'Bearer THE_ACCESS_TOKEN'
```

**Parameters**
Name|Type|Description
:-:|:-:|:-:
`old_password`|`string`|user old password
`new_password`|`string`|user new password

**Request Body**
```
{
    "old_password": "password",
    "new_password": "password01"
}
```

**Response**
```
{
    "message": "Success!"
}
```

#### 9. Delete User

**Request**
```
DELETE /user/:uuid
```

**Request Header**
```
'Authorization': 'Bearer THE_ACCESS_TOKEN'
```

**Response**
```
{
    "message": "User deleted.",
    "status": 200
}
```