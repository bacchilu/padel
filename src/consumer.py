import time
import datetime

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from libs.async_queue import Queue, Channel


database_uri = "mysql+mysqlconnector://root:luca@mysql-db/padel"
# database_uri = "mysql+mysqlconnector://root:luca@0.0.0.0/padel"


engine = create_engine(database_uri)


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)


class Slot(Base):
    __tablename__ = "slot"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)


class Booking(Base):
    __tablename__ = "booking"

    date = Column(Date, primary_key=True, index=True)
    time = Column(Integer, primary_key=True, index=True)
    slot_id = Column(Integer, ForeignKey("slot.id"), primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True, index=True)
    callback = Column(String(255))

    slot = relationship("Slot", back_populates="bookings")
    user = relationship("User", back_populates="bookings")


Slot.bookings = relationship("Booking", order_by=Booking.date, back_populates="slot")
User.bookings = relationship("Booking", order_by=Booking.date, back_populates="user")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_slots():
    session = SessionLocal()
    try:
        return session.query(Slot).all()
    finally:
        session.close()


def find_bookings(
    target_date: datetime.date,
    target_time: int,
    target_slot_id: Column[int],
    target_user_id: int | None,
):
    session = SessionLocal()
    try:
        return (
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
    finally:
        session.close()


def add_booking(
    target_date: datetime.date,
    target_time: int,
    target_user_id: int,
    slot_id: Column[int],
    callback: str,
):
    session = SessionLocal()
    try:
        session.add(
            Booking(
                date=target_date,
                time=target_time,
                user_id=target_user_id,
                slot_id=slot_id,
                callback=callback,
            )
        )
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


Channel.set_host("rabbitmq")
# Channel.set_host("0.0.0.0")


def already_booked(date: datetime.date, time: int, slot: Slot, user_id: int):
    data = find_bookings(date, time, slot.id, user_id)
    return len(data) == 1


def callback(body):
    print(f"Received message: {body}")
    date, time, user_id, callback = (
        datetime.date.fromisoformat(body["date_time"]["date"]),
        body["date_time"]["time"],
        body["user_id"],
        body["callback"]["value"],
    )
    for slot in get_slots():
        if already_booked(date, time, slot, user_id):
            print("Gia`Prenotato!", slot.id)
            continue

        data = find_bookings(date, time, slot.id, None)
        if len(data) < 4:
            add_booking(date, time, user_id, slot.id, callback)
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
