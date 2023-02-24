import sys

sys.path.append("..")

from fastapi import Depends, APIRouter, Request, Response, HTTPException
from Modules import auth
from sqlalchemy.orm import Session
from models import model
from schemas import schema

router = APIRouter(
    prefix="/application",
    tags=["application"],
    responses={401: {"user": "Not Authorised"}},
)


@router.get("/getuser")  # function
async def get_user(db: Session = Depends(auth.get_db),
                   user: None = Depends(auth.get_current_user)):  # Depends() is local dependency
    if user is None:
        # return {"reactNavigateTo": "/localhost:8000", "msg": "could not varify token/cookie"}
        raise HTTPException(status_code=401, detail="Sorry you are Unauthorized !")
    userDetails = db.get(model.User, user.get("id"))
    # print(userDetails.person.name)
    # if(userDetails.personRole.name!="ADMIN"):
    #     raise HTTPException(status_code=403, detail="Forbidden !")
    # personUser = db.query(model.Person).filter(model.Person.id == userDetails.person_id).first()
    return {"nameOfUser": userDetails.person.name, "role": userDetails.personRole.name}


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


@router.post("/createperson")
async def create_person(person: schema.person, db: Session = Depends(auth.get_db)):
    if person.name == '' or person.phone_no == '':
        return {"msg": "Name and Phone no cant be Emty"}

    db_person = db.query(model.Person).filter(
        model.Person.name == person.name).filter(model.Person.phone_no == person.phone_no).first()

    if db_person:
        print(person.name)
        raise HTTPException(status_code=400, detail="Person with same name and phone no. Already Exist")
    db_person = model.Person(**person.dict())  # maps the data
    db.add(db_person)
    db.commit()
    # db.refresh(db_person)
    return {"msg": "Person Created"}


@router.post("/createuser")
async def create_user(user: schema.create_user, db: Session = Depends(auth.get_db)):
    person = db.get(model.Person, user.person_id)  # search in person if exist
    if not person:
        raise HTTPException(status_code=404, detail=f"Person with id {user.person_id} not found")
    db_user = db.query(model.User).filter(model.User.person_id == user.person_id).first()
    if db_user:
        raise HTTPException(status_code=404, detail=f"Person id {user.person_id} Already Registered")
    db_user = db.query(model.User).filter(model.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=404, detail=f"Username already taken")

    create_user_model = model.User()
    create_user_model.username = user.username
    create_user_model.hashed_password = auth.get_password_hash(user.password)
    create_user_model.role_id = user.role_id
    create_user_model.person_id = user.person_id
    if user.role_id == '2':
        person.cultivator_id = 0  # 0 means self cultivator
        db.add(person)
        db.commit()

    db.add(create_user_model)
    db.commit()
    return {"msg": "User created"}


@router.get("/listusers")
async def list_users(offset: int = 0, limit: int = 50, db: Session = Depends(auth.get_db)):
    tempUsers = db.query(model.User).offset(offset).limit(limit).all()
    users: list = []
    for user in tempUsers:
        results = {"name": user.person.name, "username": user.username, "phone_no": user.person.phone_no,
                   "gender": user.person.gender, "role": user.personRole.name}
        users.append(results)
    return {"users": users}


@router.get("/listpersons")
async def list_persons(offset: int | None = 0, limit: int | None = 50, db: Session = Depends(auth.get_db)):
    tempPersons = db.query(model.Person).offset(offset).limit(limit).all()
    persons: list = []
    for person in tempPersons:
        user = db.query(model.User).filter(model.User.person_id == person.id).first()
        if user:
            role = user.personRole.name
        else:
            role = None
        results = {"id": person.id, "name": person.name, "phone_no": person.phone_no, "gender": person.gender,
                   "role": role}
        persons.append(results)
    return {"persons": persons}


@router.get("/getroles")
async def get_roles(db: Session = Depends(auth.get_db)):
    roles = db.query(model.Role).all()
    return {"roles": roles}


@router.get("/getguests")
async def get_guests(db: Session = Depends(auth.get_db)):
    tempGuests = db.query(model.Person).filter(model.Person.cultivator_id == None).all()
    guests: list = []
    for guest in tempGuests:
        results = {"id": guest.id, "name": guest.name, "phone_no": guest.phone_no, "email": guest.email,
                   "gender": guest.gender}
        guests.append(results)
    return {"guests": guests}
