import os
import sys

sys.path.append("..")

from fastapi import Depends, APIRouter, Request, Response, HTTPException, UploadFile, File
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
    return {"nameOfUser": userDetails.person.name, "role": userDetails.personRole.name, "user_id": userDetails.id,
            "person_id": userDetails.person.id}


@router.post("/createperson")
async def create_person(person: schema.person, db: Session = Depends(auth.get_db), user: None = Depends(auth.get_current_user)):
    if user is None:
        # return {"reactNavigateTo": "/localhost:8000", "msg": "could not varify token/cookie"}
        raise HTTPException(status_code=401, detail="Sorry you are Unauthorized !")
    if(person.id is None):
        db_person = db.query(model.Person).filter(
            model.Person.name == person.name).filter(model.Person.phone_no == person.phone_no).first()

        if db_person:
            raise HTTPException(status_code=400, detail="Person with same name and phone no. Already Exist")
        db_person = model.Person(**person.dict())  # maps the data
        db.add(db_person)
        db.commit()
        db.refresh(db_person) #comment here if shows error
        msg = "Person Created"
    else:
        db_person = db.get(model.Person, person.id)
        if not db_person:
            raise HTTPException(status_code=404, detail="Person Not Found")
        db_data = person.dict(exclude_unset=True)
        for key, value in db_data.items():
            setattr(db_person, key, value)
        db.add(db_person)
        db.commit()
        msg = "Person Updated"
        db.refresh(db_person) #comment here if shows error
    return {"msg": msg, "person": db_person}



# @router.get("/listusers")
# async def list_users(offset: int = 0, limit: int = 50, db: Session = Depends(auth.get_db)):
#     tempUsers = db.query(model.User).offset(offset).limit(limit).all()
#     users: list = []
#     for user in tempUsers:
#         results = {"name": user.person.name, "username": user.username, "phone_no": user.person.phone_no,
#                    "gender": user.person.gender, "role": user.personRole.name}
#         users.append(results)
#     return {"users": users}


@router.get("/getroles")
async def get_roles(db: Session = Depends(auth.get_db)):
    roles = db.query(model.Role).all()
    return {"roles": roles}


@router.post("/uploadprofilepic")
async def upload_profile_pic(file: UploadFile = File(...), db: Session = Depends(auth.get_db),
                             user: None = Depends(auth.get_current_user)):  # Depends() is local dependency

    if user is None:
        raise HTTPException(status_code=401, detail="Sorry you are Unauthorized !")
    # print(user)
    if not file.filename.lower().endswith(
            ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):  # checks only the magic number of the file
        return {"msg": "Not a Supported Picture !"}
    filename, file_extension = os.path.splitext(file.filename)
    # print(filename)
    # print(file_extension)
    user_id = user.get("id")
    file.filename = f"{user_id}{file_extension}"  # rename the file
    contents = await file.read()
    # save the file
    with open(f"profileImages/{file.filename}", "wb") as f:
        f.write(contents)
    return {"file_name": file.filename}
