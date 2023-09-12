from contextlib import contextmanager

from dataclasses import dataclass

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


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


engine = create_engine("mysql+mysqlconnector://root:luca@mysql-db/padel")
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


@dataclass
class UserData:
    id: int
    user: str


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
