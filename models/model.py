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
    name = Column(String(100))
    first_name = Column(String(100))
    middle_name = Column(String(100))
    last_name = Column(String(100))
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


class PersonRelationships(Base):
    __tablename__ = "person_relationships"

    id = Column(Integer, primary_key=True, index=True)
    relationship_name = Column(String(50))
    person_primary_id = Column(Integer, ForeignKey("person.id"), default=None)
    person_secondary_id = Column(Integer, ForeignKey("person.id"), default=None)
    reverse_relationship_name = Column(String(50))

    person_link1 = relationship("Person", foreign_keys=[person_primary_id])
    person_link2 = relationship("Person", foreign_keys=[person_secondary_id])


class RelationshipNames(Base):
    __tablename__ = "relationship_names"

    id = Column(Integer, primary_key=True, index=True)
    relationship_name_wrt_primary_id = Column(String(100))
    relationship_name_wrt_secondary_id = Column(String(100))

# class DummyPMSdata(Base):
#     __tablename__ = "dummy_pms_data"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50))
#     phone_no = Column(String(15))


# //---------------------relationship testing models- below--------------------------------
# class Individual(Base):
#     __tablename__ = "individual"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50))
#     phone_no = Column(String(15))
#
# class IndividualRelationship(Base):
#     __tablename__ = "individual_relationship"
#
#     id = Column(Integer, primary_key=True, index=True)
#     relationship_name = Column(String(50))
#     individual_id1 = Column(Integer, ForeignKey("individual.id"), default=None)
#     individual_id2 = Column(Integer, ForeignKey("individual.id"), default=None)
#
#     individual_link1 = relationship("Individual", foreign_keys=[individual_id1])
#     individual_link2 = relationship("Individual", foreign_keys=[individual_id2])

# //-----------relationship testing model - ends---------------------------------------------------------
