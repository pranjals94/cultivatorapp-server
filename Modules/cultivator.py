from fastapi import Depends, APIRouter, Request, Response, HTTPException
from Modules import auth
from sqlalchemy.orm import Session
from models import model
from schemas import schema
from sqlalchemy import or_, and_, exists
import sys
sys.path.append("..")

router = APIRouter(
    prefix="/cultivator",
    tags=["cultivator"],
    responses={401: {"user": "Not Authorised"}},
)

@router.get("/assigned_persons/{cultivator_id}")
async def get_guests(cultivator_id: int, db: Session = Depends(auth.get_db)):
    user = db.query(model.User).filter(model.User.role_id == 2).filter(model.User.person_id == cultivator_id).first()
    if user == None:
        return {"msg": "Cultivator not found"}
    # assigned_persons = db.query(model.Person).filter(model.Person.cultivator_id == cultivator_id).offset(0).limit(
    #     50).all()

    # below list for currently checked in visitors assigned to a cultivator
    assigned_persons = db.query(model.Person).filter(model.Visit.person_id==model.Person.id).all()

    totalGuests = db.query(model.Person).filter(model.Visit.person_id==model.Person.id).count()
    return {"guests": assigned_persons, "totalGuests": totalGuests}

    #below list for all visitors assigned to a cultivator
    # assigned_persons = db.query(model.Person).filter(model.Person.cultivator_id==cultivator_id).all()
    # return {"assigned_persons": assigned_persons}
@router.get("/assigned_persons_all/{cultivator_id}")
async def get_guests(cultivator_id: int, db: Session = Depends(auth.get_db)):
    user = db.query(model.User).filter(model.User.role_id == 2).filter(model.User.person_id == cultivator_id).first()
    if user == None:
        return {"msg": "Cultivator not found"}
    # assigned_persons = db.query(model.Person).filter(model.Person.cultivator_id == cultivator_id).offset(0).limit(
    #     50).all()

    # below list for currently checked in visitors assigned to a cultivator
    # assigned_persons = db.query(model.Person).filter(model.Visit.person_id==model.Person.id).all()
    # return {"assigned_persons": assigned_persons}

    #below list for all visitors assigned to a cultivator
    assigned_persons = db.query(model.Person).filter(model.Person.cultivator_id==cultivator_id).all()
    totalGuests = db.query(model.Person).filter(model.Person.cultivator_id==cultivator_id).count()
    return {"guests": assigned_persons, "totalGuests": totalGuests}


@router.get("/getguests")
async def get_guests(cultivator_id: int, currentPage: int, pageSize: int, db: Session = Depends(auth.get_db)):
    offset = pageSize * (currentPage - 1)
    roleCultivator = db.query(model.Role.id).filter(model.Role.name == 'CULTIVATOR')

    user = db.query(model.User).filter(model.User.role_id == roleCultivator).filter(
        model.User.person_id == cultivator_id).first()
    if user is None:
        return {"msg": "Cultivator not found"}

    totalGuests = db.query(model.Person).filter(model.Visit.person_id == model.Person.id).count()

    tempGuests = db.query(model.Person).filter(model.Visit.person_id == model.Person.id).order_by(
        model.Person.id.desc()).offset(offset).limit(pageSize).all()

    guests: list = []
    for guest in tempGuests:
        results = {"id": guest.id, "name": guest.name, "phone_no": guest.phone_no, "email": guest.email,
                   "gender": guest.gender}
        guests.append(results)

    return {"guests": guests, "totalGuests": totalGuests}

@router.get("/getassignees")
async def get_guests(cultivator_id: int, currentPage: int, pageSize: int, db: Session = Depends(auth.get_db)):
    offset = pageSize * (currentPage - 1)
    roleCultivator = db.query(model.Role.id).filter(model.Role.name == 'CULTIVATOR')

    user = db.query(model.User).filter(model.User.role_id == roleCultivator).filter(
        model.User.person_id == cultivator_id).first()
    if user is None:
        return {"msg": "Cultivator not found"}

    totalGuests = db.query(model.Person).filter(model.Person.cultivator_id==cultivator_id).count()

    tempGuests = db.query(model.Person).filter(model.Person.cultivator_id==cultivator_id).order_by(
        model.Person.id.desc()).offset(offset).limit(pageSize).all()

    guests: list = []
    for guest in tempGuests:
        results = {"id": guest.id, "name": guest.name, "phone_no": guest.phone_no, "email": guest.email,
                   "gender": guest.gender}
        guests.append(results)

    return {"guests": guests, "totalGuests": totalGuests}


@router.get("/searchAll")
async def search( cultivator_id: int =0, currentPage: int = 1, pageSize: int = 10, search_input: str = '', db: Session = Depends(auth.get_db)):
    searchData = f'%{search_input}%'
    if searchData == '%%':
        # return {"msg": "Empty search value."}
        raise HTTPException(status_code=404, detail="Empty Search value!")
    offset = pageSize * (currentPage - 1)
    persons = db.query(model.Person).filter(model.Person.cultivator_id == cultivator_id).filter(
        or_(model.Person.name.ilike(searchData),
            model.Person.phone_no.ilike(
                searchData))).offset(offset).limit(pageSize).all()
    totalGuests = db.query(model.Person).filter(or_(model.Person.name.ilike(searchData),
                                                    model.Person.phone_no.ilike(
                                                        searchData))).count()
    return {"guests": persons, "totalGuests": totalGuests}

@router.get("/search")
async def search( cultivator_id: int =0, currentPage: int = 1, pageSize: int = 10, search_input: str = '', db: Session = Depends(auth.get_db)):
    searchData = f'%{search_input}%'
    if searchData == '%%':
        # return {"msg": "Empty search value."}
        raise HTTPException(status_code=404, detail="Empty Search value!")
    offset = pageSize * (currentPage - 1)
    persons = db.query(model.Person).filter(model.Visit.person_id == model.Person.id).order_by(
                model.Person.id.desc()).filter(or_(model.Person.name.ilike(searchData),
            model.Person.phone_no.ilike(searchData))).offset(offset).limit(pageSize).all()
    totalGuests = db.query(model.Person).filter(model.Visit.person_id == model.Person.id).filter(or_(model.Person.name.ilike(searchData),
                model.Person.phone_no.ilike(searchData))).count()
    return {"guests": persons, "totalGuests": totalGuests}

