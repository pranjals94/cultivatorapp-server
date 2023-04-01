from datetime import datetime
import sys
import time

from sqlalchemy import and_
from schemas import schema

sys.path.append("..")

from fastapi import Depends, APIRouter, Request, Response, HTTPException
from Modules import auth
from sqlalchemy.orm import Session
from models import model

router = APIRouter(
    prefix="/orientation",
    tags=["orientation"],
    responses={401: {"user": "Not Authorised"}},
)


@router.get("/getlist")
async def get_list(db: Session = Depends(auth.get_db), User: None = Depends(auth.get_current_user)):
    persons = db.query(model.Person).filter(model.Person.cultivator_id != None).all()
    for item in persons:  # remove the cultivators
        if item.cultivator_id == 0:
            persons.remove(item)
    return {"persons": persons}


@router.get("/getorientations")
async def get_list(db: Session = Depends(auth.get_db), User: None = Depends(auth.get_current_user)):
    orientations = db.query(model.Orientation).all()
    return {"orientations": orientations}


@router.get("/getparticipants")
async def search(orientation_id: int, db: Session = Depends(auth.get_db)):
    participants = db.query(model.OrientationParticipants).filter(
        model.OrientationParticipants.orientation_id == orientation_id).all()
    return {"participants": participants}


@router.get("/markAttendance")
async def search(participant_id: int, db: Session = Depends(auth.get_db)):
    db_person = db.get(model.OrientationParticipants, participant_id)
    db_person.check_in_time = time.strftime("%H:%M:%S", time.localtime())
    db_person.attended = True
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    print(db_person)
    return {"participants": "Attendance Marked"}


@router.post("/addvisitor")
async def search(add_visitor: schema.add_visitor, db: Session = Depends(auth.get_db)):
    db_person = db.query(model.Person).filter(
        and_(model.Person.name == add_visitor.visitor_name, model.Person.phone_no == add_visitor.phone_no)).first()
    if not db_person:  # if person does not exist
        db_person = model.Person(
            name=add_visitor.visitor_name,
            phone_no=add_visitor.phone_no
        )
        db.add(db_person)
        db.commit()
        db.refresh(db_person)

    db_visit = model.Visit(
        person_id=db_person.id,
        check_in_date_time=datetime.now(),
        orientation_assigned=True
    )
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)

    # add to orientation
    participant = model.OrientationParticipants(
        orientation_id=add_visitor.orientation_id,
        visit_id=db_visit.id,
        visitor_name=db_person.name
    )
    db.add(participant)
    db.commit()
    db.refresh(participant)

    return {"msg": "Visitor Added."}
