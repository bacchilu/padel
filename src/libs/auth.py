import os
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field

from flask import Request
import jwt

from .database import DBModel


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
    res = DBModel.get_user_by(payload.id)
    if res is None:
        raise Exception("User not found")
    return res
