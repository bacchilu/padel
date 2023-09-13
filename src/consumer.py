import datetime

import requests

from libs.db_model import DBModel
from libs.data_types import BookingRequests, TimeSlot, Callback, SlotData, UserData
from libs.async_queue import Queue
from libs.utils import reconnection_decorator, log_console
from libs.mail_sender import send_mail as mail_send


def http_post(url: str, data: dict):
    requests.post(url, json=data)


def send_mail(mail: str, msg: str):
    log_console(f"Sending email to '{mail}': \"{msg}\"")
    mail_send(mail, msg)


class Trigger:
    @staticmethod
    def send_notification(
        user: UserData,
        time_slot: TimeSlot,
        user_callback: Callback,
        slot: SlotData | None,
    ):
        if user_callback.type == "EMAIL":
            send_mail(
                user_callback.value,
                f"Dear {user.user}, the slot {slot.name} is available for {time_slot.isoformat()}"
                if slot is not None
                else f"Dear {user.user}, we don't have a slot available for {time_slot.isoformat()}",
            )
        if user_callback.type == "URL":
            http_post(
                user_callback.value,
                {
                    "user_id": user.id,
                    "time_slot": time_slot.isoformat(),
                    "result": slot is not None,
                },
            )


class TaskManager:
    @staticmethod
    def already_booked(slot_id: int, user_id: int, time_slot: TimeSlot):
        data = DBModel.find_bookings(slot_id, user_id, time_slot)
        return len(data) == 1

    @staticmethod
    def eventually_insert(
        slot: SlotData, user_id: int, time_slot: TimeSlot, user_callback: Callback
    ):
        data = DBModel.find_bookings(slot.id, None, time_slot)
        if len(data) < 4:
            DBModel.add_booking(slot.id, user_id, time_slot, user_callback.value)
            return True
        return False

    @staticmethod
    def eventually_trigger(slot: SlotData, time_slot: TimeSlot):
        bookings = DBModel.find_bookings(slot.id, None, time_slot)
        if len(bookings) == 4:
            for booking in bookings:
                user = DBModel.get_user_by(booking.data.user_id)
                if user is None:
                    continue
                Trigger.send_notification(user, time_slot, booking.data.callback, slot)

    @staticmethod
    def execute(user_id: int, time_slot: TimeSlot, user_callback: Callback):
        user = DBModel.get_user_by(user_id)
        if user is None:
            return

        if time_slot.is_expired():
            log_console("TimeSlot Scaduto!")
            Trigger.send_notification(user, time_slot, user_callback, None)
            return

        for slot in DBModel.get_all_slots():
            if TaskManager.already_booked(slot.id, user_id, time_slot):
                log_console("Gia`Prenotato!", slot.id)
                Trigger.send_notification(user, time_slot, user_callback, None)
                return

            if TaskManager.eventually_insert(slot, user_id, time_slot, user_callback):
                TaskManager.eventually_trigger(slot, time_slot)
                return

        log_console("Non c'è posto")
        Trigger.send_notification(user, time_slot, user_callback, None)


def callback(body: dict):
    log_console(f"Received message: {body}")

    user_id: int = body["user_id"]
    time_slot = TimeSlot(
        date=datetime.date.fromisoformat(body["time_slot"]["date"]),
        time=body["time_slot"]["time"],
    )
    user_callback = BookingRequests.check_email_or_url(body["callback"]["value"])

    TaskManager.execute(user_id, time_slot, user_callback)


@reconnection_decorator(max_retries=10, delay_seconds=5)
def listen_queue(callback):
    Queue.start_consuming(callback)


if __name__ == "__main__":
    log_console("Consumer started...")
    listen_queue(callback)
