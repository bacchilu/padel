import datetime

from libs.db_model import DBModel
from libs.data_types import BookingRequests, TimeSlot, Callback, SlotData
from libs.async_queue import Queue
from libs.utils import reconnection_decorator, log_console


class Trigger:
    pass


def already_booked(slot_id: int, user_id: int, time_slot: TimeSlot):
    data = DBModel.find_bookings(slot_id, user_id, time_slot)
    return len(data) == 1


def eventually_insert(
    slot: SlotData, user_id: int, time_slot: TimeSlot, user_callback: Callback
):
    data = DBModel.find_bookings(slot.id, None, time_slot)
    if len(data) < 4:
        DBModel.add_booking(slot.id, user_id, time_slot, user_callback.value)
        return True
    return False


def eventually_trigger(slot: SlotData, time_slot: TimeSlot):
    data = DBModel.find_bookings(slot.id, None, time_slot)
    if len(data) == 4:
        log_console("Trigger callback for", data)


def execute_task(user_id: int, time_slot: TimeSlot, user_callback: Callback):
    if time_slot.is_expired():
        log_console("TimeSlot Scaduto!")
        return

    for slot in DBModel.get_all_slots():
        if already_booked(slot.id, user_id, time_slot):
            log_console("Gia`Prenotato!", slot.id)
            return

        if eventually_insert(slot, user_id, time_slot, user_callback):
            log_console("Inserito", slot.id)
            eventually_trigger(slot, time_slot)
            return

    log_console("Non c'è posto")


def callback(body: dict):
    log_console(f"Received message: {body}")

    user_id: int = body["user_id"]
    time_slot = TimeSlot(
        date=datetime.date.fromisoformat(body["time_slot"]["date"]),
        time=body["time_slot"]["time"],
    )
    user_callback = BookingRequests.check_email_or_url(body["callback"]["value"])

    execute_task(user_id, time_slot, user_callback)


@reconnection_decorator(max_retries=10, delay_seconds=5)
def listen_queue(callback):
    Queue.start_consuming(callback)


if __name__ == "__main__":
    log_console("Consumer started...")
    listen_queue(callback)
