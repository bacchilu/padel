import time


from libs import database


def create_all(timeout=1):
    try:
        database.Base.metadata.create_all(bind=database.engine, checkfirst=True)
    except:
        print("Try again...")
        time.sleep(timeout + 1)
        create_all()


if __name__ == "__main__":
    create_all()

    with database.getSession() as session:
        session.add(database.User(id=1, name="Luca", email="bacchilu@gmail.com"))
        session.add(database.User(id=2, name="Viola", email="viola@example.com"))

        session.add(database.Slot(id=1, name="Slot 1"))
        session.add(database.Slot(id=2, name="Slot 2"))
        session.add(database.Slot(id=3, name="Slot 3"))
        session.add(database.Slot(id=4, name="Slot 4"))
