from libs.async_queue import Queue, Channel


Channel.set_host("0.0.0.0")


def callback(body):
    print(f"Received message: {body}")


if __name__ == "__main__":
    print("Up and running!")
    Queue.start_consuming(callback)
