import os
import re
from datetime import datetime, date
from dataclasses import dataclass, asdict
from typing import Literal

from flask import Flask, request, jsonify

from auth import check_auth
from utils import log_console


app = Flask(__name__)


@dataclass(kw_only=True)
class TimeSlot:
    date: date
    time: int

    @classmethod
    def from_iso(cls, iso_str):
        d = datetime.fromisoformat(iso_str)
        if 9 <= d.hour <= 23:
            return cls(date=d.date(), time=d.hour)
        raise Exception("Wrong data format")


@dataclass(kw_only=True)
class Callback:
    type: Literal["EMAIL", "URL"]
    value: str


@dataclass(kw_only=True)
class BookingRequests:
    giorni: list[TimeSlot]
    callback: Callback

    @staticmethod
    def check_email_or_url(input_string: str):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        url_pattern = r"^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$"
        if re.match(email_pattern, input_string):
            return Callback(type="EMAIL", value=input_string)
        elif re.match(url_pattern, input_string):
            return Callback(type="URL", value=input_string)
        raise Exception("Wrong data format")

    @classmethod
    def from_dict(cls, json_data):
        return cls(
            giorni=[TimeSlot.from_iso(d) for d in json_data["giorni"]],
            callback=cls.check_email_or_url(json_data["callback"]),
        )


@app.route("/")
def hello_world():
    return f"Hello, Flask! - 1.0.0 ({os.environ.get('MODE')})"


@app.route("/disponibilita", methods=["POST"])
def post_booking():
    try:
        user = check_auth(request)
    except Exception as e:
        return jsonify({"message": str(e)}), 401

    try:
        data = BookingRequests.from_dict(request.json)
        log_console(user)
        log_console(data)
        return jsonify(asdict(data))
    except Exception as e:
        return jsonify({"message": str(e)}), 500
