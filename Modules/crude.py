from fastapi import APIRouter, Depends, HTTPException

from schemas import schema
from Common import services
from models import model
from Modules import auth
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/createvisitor")
async def create_visitor(person: schema.person, db: Session = Depends(services.get_database_session)):
    db_person = db.query(model.Person).filter(
        model.Person.name == person.name or model.Person.phone_no == person.phone_no).first()
    if db_person:
        raise HTTPException(status_code=400, detail="Visitor with same name and phone no. Already Exist")
    db_person = model.Person(**person.dict())  # maps the data
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


@router.post("/update")
async def update(person: schema.person, db: Session = Depends(services.get_database_session)):
    db_person = db.get(model.Person, person.id)
    if not db_person:
        raise HTTPException(status_code=404, detail="Visitor Not Found")
    db_data = person.dict(exclude_unset=True)
    for key, value in db_data.items():
        setattr(db_person, key, value)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return {"msg": "updated ok", "data": db_person}


@router.post("/create/user")
async def create_new_user(user: schema.create_user, db: Session = Depends(auth.get_db)):
    visitor = db.get(model.Person, user.person_id)  # search in person if exist
    if not visitor:
        raise HTTPException(status_code=404, detail=f"Guest/Visitor with id {user.person_id} not found")
    db_user = db.query(model.User).filter(model.User.person_id == user.person_id).first()
    if db_user:
        raise HTTPException(status_code=404, detail=f"Guest/Visitor id {user.person_id} Already Registered")
    db_user = db.query(model.User).filter(model.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=404, detail=f"Username already taken")

    create_user_model = model.User()
    create_user_model.username = user.username
    create_user_model.hashed_password = auth.get_password_hash(user.password)
    create_user_model.role = user.role
    create_user_model.person_id = user.person_id

    db.add(create_user_model)
    db.commit()
    return "User created"


@router.post("/login")
async def log_in_for_access_token(form_data: schema.log_in, db: Session = Depends(auth.get_db)):
    user = auth.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    token_expires = timedelta(minutes=20)
    token = auth.create_access_token(user.username, user.id, expires_delta=token_expires)
    return {"token": token}


@router.get("/user")
async def read_all_by_user(user: dict = Depends(auth.get_current_user),
                           db: Session = Depends(auth.get_db)):
    if user is None:
        raise auth.get_user_exception()
    # print(user.get("id"))
    userTemp = db.get(model.User, user.get("id"))
    return db.get(model.Person, userTemp.person_id)
