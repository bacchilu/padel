from dataclasses import dataclass

from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    email = Column(String(255), unique=True)


@dataclass
class UserData:
    id: int
    user: str


class DBModel:
    @staticmethod
    def get_user_by(id: int):
        user = User.query.get(id)
        return None if user is None else UserData(id=user.id, user=user.name)
