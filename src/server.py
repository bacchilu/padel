import os

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def hello_world():
    return f"Hello, Flask! - 1.0.0 ({os.environ.get('MODE')})"


@app.route("/disponibilita", methods=["POST"])
def post_disponibilita():
    data = request.json
    return jsonify({"message": "Booking request received", "data": data})
