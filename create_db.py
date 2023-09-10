from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace 'your_database_uri_here' with your actual database URI
# Example URIs:
# PostgreSQL: 'postgresql://username:password@localhost/database_name'
# MySQL: 'mysql+mysqlconnector://username:password@localhost/database_name'
# SQLite: 'sqlite:///mydatabase.db'
database_uri = "mysql+mysqlconnector://root:luca@0.0.0.0/padel"

# Create a SQLAlchemy engine
engine = create_engine(database_uri)


# Create a base class for declarative class definitions
Base = declarative_base()


# Define the User table
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)


# Create the database tables
Base.metadata.create_all(bind=engine, checkfirst=True)

# Create a Session class to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


session = SessionLocal()

try:
    # Create user instances and add them to the session
    user1 = User(id=1, name="Luca", email="bacchilu@gmail.com")
    user2 = User(id=2, name="Viola", email="viola@example.com")

    session.add(user1)
    session.add(user2)

    # Commit the changes to the database
    session.commit()
except Exception as e:
    # Handle any exceptions or errors that may occur during the process
    print(f"Error: {e}")
    session.rollback()
finally:
    # Close the session
    session.close()
