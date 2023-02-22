from sqlalchemy import Boolean, Column, Date, Integer, String, ForeignKey, Text,DateTime,DECIMAL
from sqlalchemy.orm import relationship
from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("person.personid"))
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    todos = relationship("Todos", back_populates="owner")
    created      = Column(DateTime)
    modified     = Column(DateTime)
    createdby    = Column(Integer)
    modifiedby   = Column(Integer)

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="todos")
    created      = Column(DateTime)
    modified     = Column(DateTime)
    createdby    = Column(Integer)
    modifiedby   = Column(Integer)
    is_active = Column(Boolean, default=True)

class Person(Base):
    __tablename__ = "person"

    personid     = Column(Integer, primary_key=True, index=True)
    cultivatorid = Column(Integer)
    familyid     = Column(Integer)
    familyheadid = Column(Integer)
    relation2head= Column(String(20))
    contact_no1  = Column(String(100))
    email        = Column(String(50), index=True)
    fullname     = Column(String(100), index=True)
    first_name   = Column(String(100))
    last_name    = Column(String(100))
    dateofbirth  = Column(Date)
    gender       = Column(String(10))
    station_name = Column(String(100))  
    locality_name= Column(String(100))
    city_name    = Column(String(100))
    district_name= Column(String(100))
    state_name   = Column(String(100))
    country_name = Column(String(100))
    zip_no       = Column(String(100))
    placeslived  = Column(String(100))
    city_current = Column(String(100))
    city_birth   = Column(String(100))
    is_active    = Column(Boolean, default=True)
    is_local     = Column(Boolean, default=False)    
    contact_no2  = Column(String(100))
    whatsapp_no  = Column(String(100))
    email_personal= Column(String(100))
    email_work   = Column(String(100))    
    visitortype  = Column(Integer)
    age          = Column(Integer)
    created      = Column(DateTime)
    modified     = Column(DateTime)
    createdby    = Column(Integer)
    modifiedby   = Column(Integer)
    
class Visit(Base):
    __tablename__ = "visit"

    visitid     = Column(Integer, primary_key=True, index=True)
    personid    = Column(Integer)
    tourguideid = Column(Integer)
    location    = Column(String(50))
    checkin     = Column(DateTime)
    checkout    = Column(DateTime)
    visit_no    = Column(Integer)
    groupsize   = Column(Integer)
    Room_no     = Column(String(100))
    is_active   = Column(Boolean, default=True)

class Orientation(Base):
    __tablename__ = "orientation"

    orientationid     = Column(Integer, primary_key=True, index=True)
    orientorid        = Column(Integer)
    tourguideid       = Column(Integer)
    ornassistid       = Column(Integer)
    location          = Column(String(50))
    starttime         = Column(DateTime)
    endtime           = Column(DateTime)
    
    orncapacity       = Column(Integer)
    room_no           = Column(String(100))
    building_no       = Column(String(100))
    created           = Column(DateTime)
    modified          = Column(DateTime)
    createdby         = Column(Integer)
    modifiedby        = Column(Integer)
    is_active         = Column(Boolean, default=True)

class OrnAttendance(Base):
    __tablename__ = "ornattendance"

    orientationid     = Column(Integer,primary_key=True,  index=True)
    participantid     = Column(Integer,primary_key=True,index=True)
    orientorid        = Column(Integer)
    intime            = Column(DateTime)
    outtime           = Column(DateTime)
    created           = Column(DateTime)
    modified          = Column(DateTime)
    createdby         = Column(Integer)
    modifiedby        = Column(Integer)
    is_active = Column(Boolean, default=True)

class UserRole(Base):
    __tablename__ = "userrole"

    roleid           = Column(Integer,primary_key=True,  index=True)
    permissionid     = Column(Integer,primary_key=True,index=True)
    rolename         = Column(String(100))
    is_active        = Column(Boolean, default=True)

class UserPermission(Base):
    __tablename__ = "userpermission"

    permissionid             = Column(Integer,primary_key=True,  index=True)
    permissionname           = Column(String(100))
    moduleaccessname         = Column(String(100))
    moduleaccesstype         = Column(String(100))
    is_active                = Column(Boolean, default=True)

class UserCommunication(Base):
    __tablename__ = "usercommunication"

    communicationtypeid         = Column(Integer,primary_key=True,  index=True)
    communicationname           = Column(String(100))
    communicationtype           = Column(String(10))
    is_active                   = Column(Boolean, default=True)

class UserRoleMap(Base):
    __tablename__ = "userrolemap"

    roleid            = Column(Integer,primary_key=True,  index=True)
    userid            = Column(Integer,primary_key=True,index=True)
    rolename          = Column(String(100))
    locality_role     = Column(String(100))
    city_role         = Column(String(100))
    created           = Column(DateTime)
    modified          = Column(DateTime)
    createdby         = Column(Integer)
    modifiedby        = Column(Integer)
    is_active         = Column(Boolean, default=True)

class PersonGroupMap(Base):
    __tablename__ = "persongroupmap"

    groupid           = Column(Integer,primary_key=True,  index=True)
    personid          = Column(Integer,primary_key=True,index=True)
    created           = Column(DateTime)
    modified          = Column(DateTime)
    createdby         = Column(Integer)
    modifiedby        = Column(Integer)
    is_active         = Column(Boolean, default=True)
 
class CommunicationStatus(Base):
    __tablename__ = "communciationstatus"  

    commstatusid   = Column(Integer,primary_key=True,  index=True)
    commstatusname = Column(String(100))
    description    = Column(String(100))
    

class CommunicationLog(Base):
    __tablename__ = "communciationlog"

    communicationid   = Column(Integer,primary_key=True,  index=True)
    cultivatorid      = Column(Integer)
    visitorid         = Column(Integer)
    togroupid         = Column(Integer)
    starttime         = Column(DateTime)
    endtime           = Column(DateTime)
    commstatusid      = Column(Integer)
    commdescription   = Column(String(100))
    commtopic         = Column(String(100))
    commdirection     = Column(String(100))
    commlocation      = Column(String(100))
    remindernum       = Column(Integer)
    remindersettime   = Column(DateTime)
    created           = Column(DateTime)
    modified          = Column(DateTime)
    createdby         = Column(Integer)
    modifiedby        = Column(Integer)
    is_active = Column(Boolean, default=True)

class Family(Base):
    __tablename__ = "family"

    familyid             = Column(Integer,primary_key=True,  index=True)
    familyname           = Column(String(100), unique=True)
    fammilysize          = Column(Integer)
    is_active            = Column(Boolean, default=True)
    created           = Column(DateTime)
    modified          = Column(DateTime)
    createdby         = Column(Integer)
    modifiedby        = Column(Integer)

class Group(Base):
    __tablename__ = "group"

    groupid             = Column(Integer,primary_key=True,  index=True)
    groupname           = Column(String(100))
    groupdescription    = Column(String(100))
    is_active           = Column(Boolean, default=True)
    created           = Column(DateTime)
    modified          = Column(DateTime)
    createdby         = Column(Integer)
    modifiedby        = Column(Integer)

class Event(Base):
    __tablename__ = "event"

    eventid             = Column(Integer,primary_key=True,  index=True)
    eventname           = Column(String(30))
    eventdescription    = Column(String(100))     
    eventtype           = Column(Integer) 
    is_active           = Column(Boolean, default=True)
    created           = Column(DateTime)
    modified          = Column(DateTime)
    createdby         = Column(Integer)
    modifiedby        = Column(Integer)

class Activity(Base):
    __tablename__ = "activity"

    activityid             = Column(Integer,primary_key=True,  index=True)
    activityname           = Column(String(30))
    activitydescription    = Column(String(100))     
    activitytype           = Column(Integer) 
    aktvtstartdttime       = Column(DateTime)
    aktvtfinishdttime      = Column(DateTime) 
    is_active              = Column(Boolean, default=True)
    created           = Column(DateTime)
    modified          = Column(DateTime)
    createdby         = Column(Integer)
    modifiedby        = Column(Integer)

class TempleCalendar(Base):
    __tablename__ = "templecalendar"

    activityid        = Column(Integer,primary_key=True,  index=True)
    eventid           = Column(Integer)
    startdt           = Column(DateTime)
    finishdt          = Column(DateTime)    
    is_complete       = Column(Boolean, default=False)
    zone              = Column(String(20))

class VisitorEvent(Base):
    __tablename__ = "visitorevent"

    rowid             = Column(Integer, primary_key=True)
    activityid        = Column(Integer)
    eventid           = Column(Integer)
    person_id         = Column(Integer)
    group_id          = Column(Integer)
    family_id         = Column(Integer)    
    startdt           = Column(DateTime)
    finishdt          = Column(DateTime)    
    is_complete       = Column(Boolean, default=False)
    locality          = Column(String(20))
    location          = Column(String(20))

class NewsFeed(Base):
    __tablename__ = "newsfeed"

    activityid        = Column(Integer,primary_key=True,  index=True)
    eventid           = Column(Integer)
    startdt           = Column(DateTime)
    finishdt          = Column(DateTime)    
    is_complete       = Column(Boolean, default=False)
    targetvisitortype = Column(String(20))
    location          = Column(String(20))

class Volunteering(Base):
    __tablename__ = "volunteering"

    activityid        = Column(Integer,primary_key=True,  index=True)
    eventid           = Column(Integer)
    visitorid         = Column(Integer)
    groupid           = Column(Integer)
    startdt           = Column(DateTime)
    finishdt          = Column(DateTime)    
    is_complete       = Column(Boolean, default=False)
    priority          = Column(Integer)
    location          = Column(String(20))

class spiritualState(Base):
    __tablename__ = "spiritualstate"

    visitorid         = Column(Integer,primary_key=True,  index=True)
    activityid        = Column(Integer,primary_key=True,  index=True)
    cultivatorid      = Column(Integer)
    startdt           = Column(DateTime)
    finishdt          = Column(DateTime)  
    discontinuedt     = Column(DateTime)    
    is_complete       = Column(Boolean, default=False)
    level             = Column(Integer)
    location          = Column(String(20))

class BKGroundCheck(Base):
    __tablename__ = "bkgroundcheck"

    visitorid         = Column(Integer,primary_key=True,  index=True)
    pastjob           = Column(String(20),primary_key=True)
    qualification     = Column(String(20),primary_key=True)
    policecase        = Column(String(20),primary_key=True)
    travelhistory     = Column(String(20),primary_key=True)
    cultivatorid      = Column(Integer)
    startdt           = Column(DateTime)
    finishdt          = Column(DateTime)  
    discontinuedt     = Column(DateTime)    
    is_complete       = Column(Boolean, default=False)
    location          = Column(String(20))

class visitorLogBook(Base):
    __tablename__ = "visitorlogbook"

    logbookid         = Column(Integer,primary_key=True,  index=True)
    cultivatorid      = Column(Integer)
    visitorid         = Column(Integer)
    orientationdone   = Column(Boolean, default=False)
    donationmade      = Column(Boolean, default=False)
    pledgemade        = Column(Boolean, default=False)
    temple_event      = Column(Boolean, default=False)
    personal_event    = Column(Boolean, default=False)
    level             = Column(Integer)
    serious_casual    = Column(Boolean, default=True)
    responselevel     = Column(Integer)
    created           = Column(DateTime)
    modified          = Column(DateTime)
    createdby         = Column(Integer)
    modifiedby        = Column(Integer)
    is_active = Column(Boolean, default=True)

class DonationPledge(Base):
    __tablename__ = "donationpledge"

    pledgeid          = Column(Integer,primary_key=True,  index=True)
    cultivatorid      = Column(Integer)
    visitorid         = Column(Integer)
    pledgedate        = Column(DateTime)
    donationdate      = Column(DateTime)
    pledgeamt         = Column(DECIMAL)
    donationamt       = Column(DECIMAL)
    chequecashonline  = Column(Integer)
    donationpurpose   = Column(String(30))
    created           = Column(DateTime)
    modified          = Column(DateTime)
    createdby         = Column(Integer)
    modifiedby        = Column(Integer)
    is_complete       = Column(Boolean, default=True)



