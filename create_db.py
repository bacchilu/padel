from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


database_uri = "mysql+mysqlconnector://root:luca@0.0.0.0/padel"


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
    callback = Column(String(255), unique=True, index=True)

    slot = relationship("Slot", back_populates="bookings")
    user = relationship("User", back_populates="bookings")


Slot.bookings = relationship("Booking", order_by=Booking.date, back_populates="slot")
User.bookings = relationship("Booking", order_by=Booking.date, back_populates="user")


Base.metadata.create_all(bind=engine, checkfirst=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


session = SessionLocal()

try:
    session.add(User(id=1, name="Luca", email="bacchilu@gmail.com"))
    session.add(User(id=2, name="Viola", email="viola@example.com"))

    session.add(Slot(id=1, name="Slot 1"))
    session.add(Slot(id=2, name="Slot 2"))
    session.add(Slot(id=3, name="Slot 3"))
    session.add(Slot(id=4, name="Slot 4"))

    session.commit()
except Exception as e:
    print(f"Error: {e}")
    session.rollback()
finally:
    session.close()
