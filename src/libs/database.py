import os
from contextlib import contextmanager

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING", "")


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


engine = create_engine(DB_CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def getSession():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
