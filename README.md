# Flask-RESTful-User-Auth-API
[![Build Status](https://travis-ci.org/fatematzuhora/Flask-RESTful-User-Auth-API.svg?branch=master)](https://travis-ci.org/fatematzuhora/Flask-RESTful-User-Auth-API) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)

A simple RESTful User Auth API built using [Flask](http://flask.pocoo.org) Framework & [SQLAlchemy](http://www.sqlalchemy.org), and connecting the both using [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org) library.



### Getting started
At first you'll need to get the source code of the project. Do this by cloning the Flask-RESTful-User-Auth-API repository.

```
# get the project code
$ git clone https://github.com/fatematzuhora/Flask-RESTful-User-Auth-API.git
$ cd Flask-RESTful-User-Auth-API
```

Create a virtual environment for this project and install dependencies
```
# create a virtualenv in which we can install the dependencies
$ virtualenv .venv
$ source .venv/bin/activate
```

```
pip install -r requirements.txt
```

### Running the App

```
$ python app.py
```


### Sample .env File
```
SECRET_KEY="w&8s%5^5vuhy2-gvkyi=gg4e*tso*51mb$l!=%o(@$a2tmq6o+Flask-RESTful-User-Auth-API"
DEBUG=TRUE
SQLALCHEMY_DATABASE_URI="mysql://YOUR_DB_USER_NAME:YOUR_DB_PASS@localhost:3306/YOUR_DB_NAME"
SQLALCHEMY_TRACK_MODIFICATIONS=FALSE
SALT_KEY="TEST_SALT_KEY"
```