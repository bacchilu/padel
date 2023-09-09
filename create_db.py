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
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)


# Create the database tables
Base.metadata.create_all(bind=engine, checkfirst=True)

# Create a Session class to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
