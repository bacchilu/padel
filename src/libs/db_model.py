import datetime

from .data_types import UserData, SlotData, BookingData
from .database import getSession, User, Slot, Booking


class DBModel:
    @staticmethod
    def get_user_by(id: int):
        with getSession() as session:
            user = session.query(User).filter_by(id=id).first()
            return (
                None
                if user is None
                else UserData(id=int(str(user.id)), user=str(user.name))
            )

    @staticmethod
    def get_all_slots():
        with getSession() as session:
            return [
                SlotData(id=int(str(s.id)), name=str(s.name))
                for s in session.query(Slot).all()
            ]

    @staticmethod
    def find_bookings(
        target_date: datetime.date,
        target_time: int,
        target_slot_id: int,
        target_user_id: int | None,
    ):
        with getSession() as session:
            res = (
                session.query(Booking)
                .filter(Booking.date == target_date)
                .filter(Booking.time == target_time)
                .filter(Booking.slot_id == target_slot_id)
                .filter(
                    Booking.user_id == Booking.user_id
                    if target_user_id is None
                    else Booking.user_id == target_user_id
                )
                .all()
            )
            return [
                BookingData(
                    date=datetime.date.fromisoformat(str(r.date)),
                    time=int(str(r.time)),
                    slot_id=int(str(r.slot_id)),
                    user_id=int(str(r.user_id)),
                    callback=str(r.callback),
                )
                for r in res
            ]

    @staticmethod
    def add_booking(
        target_date: datetime.date,
        target_time: int,
        target_user_id: int,
        slot_id: int,
        callback: str,
    ):
        with getSession() as session:
            session.add(
                Booking(
                    date=target_date,
                    time=target_time,
                    user_id=target_user_id,
                    slot_id=slot_id,
                    callback=callback,
                )
            )
