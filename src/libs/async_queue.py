import json
from contextlib import contextmanager

import pika
from pika.adapters.blocking_connection import BlockingChannel

from libs.utils import log_console
from libs.data_types import BookingRequests


class Channel:
    QUEUE_NAME = "padel_queue"
    HOST = "rabbitmq"

    @classmethod
    @contextmanager
    def get_channel(cls):
        rabbitmq_parameters = pika.ConnectionParameters(
            host=Channel.HOST,
            port=5672,
            credentials=pika.PlainCredentials(username="luca", password="luca"),
        )
        with pika.BlockingConnection(rabbitmq_parameters) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=Channel.QUEUE_NAME)
            yield cls(channel)

    @classmethod
    def set_host(cls, host):
        cls.HOST = host

    def __init__(self, channel: BlockingChannel):
        self.channel = channel

    def basic_publish(self, data: dict):
        self.channel.basic_publish(
            exchange="",
            routing_key=Channel.QUEUE_NAME,
            body=json.dumps(data),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def start_consuming(self, cb):
        def callback(ch, method, properties, body):
            cb(json.loads(body))

        self.channel.basic_consume(
            queue=Channel.QUEUE_NAME, on_message_callback=callback, auto_ack=True
        )
        self.channel.start_consuming()


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

    @staticmethod
    def start_consuming(callback):
        with Channel.get_channel() as channel:
            channel.start_consuming(callback)
