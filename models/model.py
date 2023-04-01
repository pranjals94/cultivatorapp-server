import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, BIGINT, Time, Date
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(BIGINT, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    hashed_password = Column(String(200))
    date_created = Column(DateTime, default=datetime.datetime.now())
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    role_id = Column(BIGINT, ForeignKey("role.id"), default=None)
    personRole = relationship("Role", back_populates="user")

    person_id = Column(BIGINT, ForeignKey("person.id"))
    person = relationship("Person", back_populates="owner")


class Role(Base):
    __tablename__ = "role"

    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    user = relationship("User", back_populates="personRole")


class Person(Base):
    __tablename__ = "person"

    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String(100))
    first_name = Column(String(100))
    middle_name = Column(String(100))
    last_name = Column(String(100))
    phone_no = Column(BIGINT, nullable=False)
    email = Column(String(50), default=None)
    city = Column(String(50), default=None)
    gender = Column(String(50), default=None)
    dob = Column(DateTime, default=None)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.now())
    cultivator_id = Column(BIGINT, default=None)
    is_deceased = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    # last_updated_by = Column(String(50), default=None)

    owner = relationship("User", back_populates="person")


class Visit(Base):
    __tablename__ = "visit"
    id = Column(BIGINT, primary_key=True, index=True)
    version = Column(BIGINT, nullable=False)
    person_id = Column(BIGINT, ForeignKey("person.id"), default=None)
    location = Column(String(50))
    remarks = Column(String(100))
    check_in_date_time = Column(DateTime)
    check_out_date_time = Column(DateTime)
    pax = Column(BIGINT)  # no of persons in group
    accommodation = Column(String(100))
    orientation_assigned = Column(Boolean, default=False)

    created_by_id = Column(BIGINT, default=None)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated_by_id = Column(BIGINT, default=None)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)
    deleted_by_id = Column(BIGINT, default=None)

    is_active = Column(Boolean, default=True)

    __mapper_args__ = {"version_id_col": version}


class Orientation(Base):
    __tablename__ = "orientation"

    id = Column(BIGINT, primary_key=True, index=True)
    orientation_name = Column(String(50), nullable=False)
    cultivator_id = Column(BIGINT, nullable=False)
    cultivator_assistant_id = Column(BIGINT)
    orienter_id = Column(BIGINT, ForeignKey("person.id"), default=None)
    orientation_start_date_time = Column(DateTime, nullable=False)
    orientation_end_date_time = Column(DateTime, nullable=False)
    venue = Column(String(30), nullable=False)

    created_by_id = Column(BIGINT, default=None)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated_by_id = Column(BIGINT, default=None)
    last_updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    is_deleted = Column(Boolean, default=False)
    deleted_by_id = Column(BIGINT, default=None)


class OrientationParticipants(Base):
    __tablename__ = "orientation_participants"

    id = Column(BIGINT, primary_key=True, index=True)
    orientation_id = Column(BIGINT, default=None)
    visit_id = Column(BIGINT, default=None)
    visitor_name = Column(String(30))
    check_in_time = Column(Time)
    attended = Column(Boolean, default=False)


class PersonRelationships(Base):
    __tablename__ = "person_relationships"

    id = Column(BIGINT, primary_key=True, index=True)
    relationship_name = Column(String(50))
    person_primary_id = Column(BIGINT, ForeignKey("person.id"), default=None)
    person_secondary_id = Column(BIGINT, ForeignKey("person.id"), default=None)
    reverse_relationship_name = Column(String(50))

    person_link1 = relationship("Person", foreign_keys=[person_primary_id])
    person_link2 = relationship("Person", foreign_keys=[person_secondary_id])


class RelationshipNames(Base):
    __tablename__ = "relationship_names"

    id = Column(BIGINT, primary_key=True, index=True)
    relationship_name_wrt_primary_id = Column(String(100))
    relationship_name_wrt_secondary_id = Column(String(100))


# class DummyPMSdata(Base):
#     __tablename__ = "dummy_pms_data"
#
#     id = Column(BIGINT, primary_key=True, index=True)
#     name = Column(String(50))
#     phone_no = Column(String(15))


# //---------------------relationship testing models- below--------------------------------
# class Individual(Base):
#     __tablename__ = "individual"
#
#     id = Column(BIGINT, primary_key=True, index=True)
#     name = Column(String(50))
#     phone_no = Column(String(15))
#
# class IndividualRelationship(Base):
#     __tablename__ = "individual_relationship"
#
#     id = Column(BIGINT, primary_key=True, index=True)
#     relationship_name = Column(String(50))
#     individual_id1 = Column(BIGINT, ForeignKey("individual.id"), default=None)
#     individual_id2 = Column(BIGINT, ForeignKey("individual.id"), default=None)
#
#     individual_link1 = relationship("Individual", foreign_keys=[individual_id1])
#     individual_link2 = relationship("Individual", foreign_keys=[individual_id2])

# //-----------relationship testing model - ends---------------------------------------------------------

class DateTimeTest(Base):
    __tablename__ = "date_time_test"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String(50))
    date_created = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
