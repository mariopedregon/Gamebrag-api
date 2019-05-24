from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
from flask import Flask, jsonify, request
import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    __tablename__="users" # todos
    id = db.Column(db.Integer, primary_key=True)
    userRole = db.Column(db.String(25), nullable=False)
    userName = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    
    def __init__(self, userName, password, userRole):
        self.userName = userName
        self.password = password
        self.userRole = userRole

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "userName", "password")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/users", methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)

@app.route("/user<id>", methods=["GET"])
def get_user(id):
    user = db.session.query(User.id, User.userName, User.password, User.userRole).filter(User.id == id).first()
    result = user_schema.dump(user)
    return jsonify(result.data)

@app.route("/add-user", methods=["POST"])
def add_user():
    userRole = request.json["userRole"]
    userName = request.json["userName"]
    password = request.json["password"]
    record = User(userName, password, userRole)

    db.session.add(record)
    db.session.commit()

    user = User.query.get(record.id)
    return user_schema.jsonify(user)


@app.route("/user<id>", methods=["DELETE"])
def delete_user(id):
    record = db.session.query(User).get(id)
    db.session.delete(record)
    db.session.commit()

    return jsonify("Record Deleted!")

if __name__ == "__main__":
    app.debug = True
    app.run()