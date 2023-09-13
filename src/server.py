import os

from flask import Flask, request, jsonify, send_from_directory

from libs.auth import check_auth
from libs.data_types import BookingRequests
from libs.async_queue import Queue
from libs.db_model import DBModel


app = Flask(__name__)


@app.route("/")
def hello_world():
    return send_from_directory("static/dist", "index.html")
    # return f"Hello, Flask! - 1.0.0 ({os.environ.get('MODE')})"


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


@app.route("/api/slots", methods=["GET"])
def get_slots():
    try:
        slots = DBModel.get_all_slots()
        return jsonify([s.to_dict() for s in slots])
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/api/bookings", methods=["GET"])
def get_bookings():
    try:
        bookings = DBModel.get_all_bookings()
        return jsonify([b.to_dict() for b in bookings])
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    try:
        user = DBModel.get_user_by(user_id)
        return jsonify(None if user is None else user.to_dict())
    except Exception as e:
        return jsonify({"message": str(e)}), 500
