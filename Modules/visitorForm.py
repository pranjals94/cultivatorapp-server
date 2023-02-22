from fastapi import APIRouter, Depends, HTTPException
from schemas import schema
from Common import services
from models import model

from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/")  # function
async def read_root():
    return {"Hello": "Visitor"}


@router.post("/addPerson")  # function
async def addPerson(person: schema.person, db: Session = Depends(services.get_database_session)):
    db_person = db.query(model.Person).filter(
        model.Person.name == person.name).first()
    if db_person:
        raise HTTPException(status_code=400, detail="Visitor already exist")
    db_visitor = model.Person(**person.dict())  # maps the data
    db.add(db_visitor)
    db.commit()
    db.refresh(db_person)

    return {"msg": "visitor saved", "visiotor": db_visitor}
