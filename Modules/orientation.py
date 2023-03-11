import sys

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
