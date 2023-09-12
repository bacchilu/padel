import time
import datetime

from libs import database
from libs.async_queue import Queue, Channel


def get_slots(session):
    return session.query(database.Slot).all()


def find_bookings(
    session,
    target_date: datetime.date,
    target_time: int,
    target_slot_id: int,
    target_user_id: int | None,
):
    return (
        session.query(database.Booking)
        .filter(database.Booking.date == target_date)
        .filter(database.Booking.time == target_time)
        .filter(database.Booking.slot_id == target_slot_id)
        .filter(
            database.Booking.user_id == database.Booking.user_id
            if target_user_id is None
            else database.Booking.user_id == target_user_id
        )
        .all()
    )


def add_booking(
    session,
    target_date: datetime.date,
    target_time: int,
    target_user_id: int,
    slot_id: int,
    callback: str,
):
    session.add(
        database.Booking(
            date=target_date,
            time=target_time,
            user_id=target_user_id,
            slot_id=slot_id,
            callback=callback,
        )
    )


Channel.set_host("rabbitmq")
# Channel.set_host("0.0.0.0")


def already_booked(session, date: datetime.date, time: int, slot: int, user_id: int):
    data = find_bookings(session, date, time, slot, user_id)
    return len(data) == 1


def callback(body):
    with database.getSession() as session:
        print(f"Received message: {body}")
        date, time, user_id, callback = (
            datetime.date.fromisoformat(body["date_time"]["date"]),
            body["date_time"]["time"],
            body["user_id"],
            body["callback"]["value"],
        )
        for slot in get_slots(session):
            if already_booked(session, date, time, int(str(slot.id)), user_id):
                print("Gia`Prenotato!", slot.id)
                continue

            data = find_bookings(session, date, time, int(str(slot.id)), None)
            if len(data) < 4:
                add_booking(session, date, time, user_id, int(str(slot.id)), callback)
                print("Inserito", slot.id)
                break
            print("Non c'è posto", slot.id)


if __name__ == "__main__":
    print("Up and running!")
    while True:
        try:
            Queue.start_consuming(callback)
            break
        except:
            print("waiting...")
            time.sleep(1)
