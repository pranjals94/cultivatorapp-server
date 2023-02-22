from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# create a database url
DATABASE_URL = "mysql+mysqlconnector://gaura:gaura@localhost:3306/cultivator_app"
# create an sqlAlchemy engine
engine = create_engine(DATABASE_URL)
# Create a SessionLocal class
# Each instance of the SessionLocal class will be a database session. The class itself is not a database session yet.
# But once we create an instance of the SessionLocal class, this instance will be the actual database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create a Base class
# Now we will use the function declarative_base() that returns a class.
# Later we will inherit from this class to create each of the database models or classes (the ORM models):
Base = declarative_base()
