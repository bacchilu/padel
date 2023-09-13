from libs import database
from libs.utils import reconnection_decorator, log_console


@reconnection_decorator(max_retries=10, delay_seconds=5)
def create_all():
    database.Base.metadata.create_all(bind=database.engine, checkfirst=True)


if __name__ == "__main__":
    log_console("CreateDB started...")
    create_all()

    with database.getSession() as session:
        session.add(database.User(id=1, name="Luca", email="bacchilu@gmail.com"))
        session.add(database.User(id=2, name="Viola", email="viola@example.com"))

        session.add(database.Slot(id=1, name="Slot 1"))
        session.add(database.Slot(id=2, name="Slot 2"))
        session.add(database.Slot(id=3, name="Slot 3"))
        session.add(database.Slot(id=4, name="Slot 4"))

    log_console("CreateDB terminated!")
