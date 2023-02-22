import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, BIGINT
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    # role = Column(String(50), default=None)
    hashed_password = Column(String(200))
    date_created = Column(DateTime, default=datetime.datetime.now())
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    role_id = Column(Integer, ForeignKey("role.id"), default=None)
    personRole = relationship("Role", back_populates="user")

    person_id = Column(Integer, ForeignKey("person.id"))
    person = relationship("Person", back_populates="owner")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    user = relationship("User", back_populates="personRole")


class Person(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    phone_no = Column(BIGINT)
    email = Column(String(50), default=None)
    city = Column(String(50), default=None)
    gender = Column(String(50), default=None)
    dob = Column(DateTime, default=None)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.now())
    cultivator_id = Column(Integer, default=None)
    is_deceased = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    owner = relationship("User", back_populates="person")


class DummyPMSdata(Base):
    __tablename__ = "dummy_pms_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    phone_no = Column(String(15))
