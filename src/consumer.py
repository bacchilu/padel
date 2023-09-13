import datetime

from libs.db_model import DBModel
from libs.async_queue import Queue
from libs.utils import reconnection_decorator


def already_booked(date: datetime.date, time: int, slot: int, user_id: int):
    data = DBModel.find_bookings(date, time, slot, user_id)
    return len(data) == 1


def callback(body):
    print(f"Received message: {body}")
    date, time, user_id, callback = (
        datetime.date.fromisoformat(body["date_time"]["date"]),
        body["date_time"]["time"],
        body["user_id"],
        body["callback"]["value"],
    )
    for slot in DBModel.get_all_slots():
        if already_booked(date, time, int(str(slot.id)), user_id):
            print("Gia`Prenotato!", slot.id)
            continue

        data = DBModel.find_bookings(date, time, int(str(slot.id)), None)
        if len(data) < 4:
            DBModel.add_booking(date, time, user_id, int(str(slot.id)), callback)
            print("Inserito", slot.id)
            break
        print("Non c'è posto", slot.id)


@reconnection_decorator(max_retries=10, delay_seconds=5)
def listen_queue(callback):
    Queue.start_consuming(callback)


if __name__ == "__main__":
    print("Up and running!")
    listen_queue(callback)
