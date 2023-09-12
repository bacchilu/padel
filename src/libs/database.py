from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
    def get_user_by(id: int):
        user = User.query.get(id)
        return None if user is None else UserData(id=user.id, user=user.name)
