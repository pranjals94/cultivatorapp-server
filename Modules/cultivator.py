import sys

sys.path.append("..")

from fastapi import Depends, APIRouter, Request, Response, HTTPException
from Modules import auth
from sqlalchemy.orm import Session
from models import model
from schemas import schema

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
    assigned_persons = db.query(model.Person).filter(model.Person.cultivator_id == cultivator_id).offset(0).limit(
        50).all()
    return {"assigned_persons": assigned_persons}
