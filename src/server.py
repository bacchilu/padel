import os

from flask import Flask, request, jsonify

from libs.auth import check_auth
from libs.data_types import BookingRequests
from libs.async_queue import Queue


app = Flask(__name__)


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
        data = BookingRequests.from_dict(user.id, request.get_json())
        Queue.push(data)
        return jsonify(request.get_json())
    except Exception as e:
        return jsonify({"message": str(e)}), 500
