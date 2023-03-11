import sys

sys.path.append("..")

from fastapi import Depends, APIRouter, Request, Response, HTTPException
from Modules import auth
from sqlalchemy.orm import Session
from models import model
from schemas import schema
from openpyxl import Workbook

router = APIRouter(
    prefix="/reception",
    tags=["reception"],
    responses={401: {"user": "Not Authorised"}},
)


@router.post("/assign-persons-to-cultivator")
async def get_guests(obj: schema.assign_cultivator_to_persons, db: Session = Depends(auth.get_db)):
    for item in obj.persons:
        create_person_model = db.get(model.Person, item)
        create_person_model.cultivator_id = obj.cultivator.id
        db.add(create_person_model)
        db.commit()
    return {"msg": f"Persons Assigned to CULTIVATOR {obj.cultivator.name}"}


@router.get("/getcultivators")
async def get_cultivators(request: Request, db: Session = Depends(auth.get_db)):
    user = await auth.get_current_user(request)
    if user is None:
        raise HTTPException(status_code=401, detail="Sorry you are Unauthorized !")
    tempCultivators = db.query(model.User).filter(model.User.role_id == 2).offset(0).limit(
        50).all()  # role id 2 is for cultivator
    # userDetails = db.get(model.User, user.get("id"))
    # print(cultivators[2].person.name)
    # if(userDetails.personRole.name!="ADMIN"):
    #     raise HTTPException(status_code=403, detail="Forbidden !")
    # personUser = db.query(model.Person).filter(model.Person.id == userDetails.person_id).first()
    cultivators: list = []
    for cultivator in tempCultivators:
        results = {"id": cultivator.person.id, "name": cultivator.person.name}
        cultivators.append(results)
    return {"cultivators": cultivators}


@router.get("/getguests")
async def get_guests(db: Session = Depends(auth.get_db)):
    tempGuests = db.query(model.Person).filter(model.Person.cultivator_id == None).order_by(model.Person.id.desc()).all()
    guests: list = []
    for guest in tempGuests:
        results = {"id": guest.id, "name": guest.name, "phone_no": guest.phone_no, "email": guest.email,
                   "gender": guest.gender}
        guests.append(results)
    return {"guests": guests}

