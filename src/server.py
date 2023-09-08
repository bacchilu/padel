import sys
import os
import re
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Literal

from flask import Flask, request, jsonify


app = Flask(__name__)


def log_console(data: object):
    print(data, file=sys.stderr)


@dataclass(kw_only=True)
class Callback:
    type: Literal["EMAIL", "URL"]
    value: str


@dataclass(kw_only=True)
class BookingRequests:
    giorni: list[datetime]
    callback: Callback

    @staticmethod
    def check_email_or_url(input_string: str):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        url_pattern = r"^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$"
        if re.match(email_pattern, input_string):
            return Callback(type="EMAIL", value=input_string)
        elif re.match(url_pattern, input_string):
            return Callback(type="URL", value=input_string)
        assert False

    @classmethod
    def from_dict(cls, json_data):
        return cls(
            giorni=[datetime.fromisoformat(d) for d in json_data["giorni"]],
            callback=cls.check_email_or_url(json_data["callback"]),
        )


@app.route("/")
def hello_world():
    return f"Hello, Flask! - 1.0.0 ({os.environ.get('MODE')})"


@app.route("/disponibilita", methods=["POST"])
def post_booking():
    data = BookingRequests.from_dict(request.json)
    log_console(data)
    return jsonify({"message": "OK", "data": asdict(data)})
