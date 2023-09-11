import os
import json
from contextlib import contextmanager


from flask import Flask, request, jsonify
import pika
from pika.adapters.blocking_connection import BlockingChannel


from auth import check_auth
from utils import log_console
from data_types import BookingRequests


app = Flask(__name__)


class Channel:
    QUEUE_NAME = "padel_queue"
    rabbitmq_parameters = pika.ConnectionParameters(
        host="rabbitmq",
        port=5672,
        credentials=pika.PlainCredentials(username="luca", password="luca"),
    )

    def __init__(self, channel: BlockingChannel):
        self.channel = channel

    def basic_publish(self, data: dict):
        self.channel.basic_publish(
            exchange="",
            routing_key=Channel.QUEUE_NAME,
            body=json.dumps(data),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    @classmethod
    @contextmanager
    def get_channel(cls):
        with pika.BlockingConnection(Channel.rabbitmq_parameters) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=Channel.QUEUE_NAME)
            yield cls(channel)


class Queue:
    @staticmethod
    def push(data: list[BookingRequests]):
        with Channel.get_channel() as channel:
            for item in data:
                e = item.to_dict()
                try:
                    channel.basic_publish(e)
                    log_console("Data published to RabbitMQ successfully.")
                except Exception as e:
                    log_console(str(e))


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
