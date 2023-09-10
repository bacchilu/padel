import os
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field

from flask import Flask, Request
import jwt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+mysqlconnector://root:luca@mysql-db/padel"
db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)


@dataclass
class UserData:
    id: int
    user: str


class DBModel:
    @staticmethod
    def get_users(id: int):
        with app.app_context():
            user = User.query.get(id)
            return None if user is None else UserData(id=user.id, user=user.name)


@dataclass
class Payload:
    id: int
    user: str
    exp: datetime = field(
        default_factory=lambda: datetime.now(tz=timezone.utc) + timedelta(days=1)
    )


def check_jwt(request: Request):
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise Exception("Token is missing")
    token = auth_header.split(" ")[1]
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    return Payload(**payload)


def check_auth(request: Request):
    payload = check_jwt(request)
    res = DBModel.get_users(payload.id)
    if res is None:
        raise Exception("User not found")
    return res
