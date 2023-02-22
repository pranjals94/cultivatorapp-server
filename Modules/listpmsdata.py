from fastapi import APIRouter, Depends, HTTPException

from schemas import schema
from Common import services
from models import model

from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/getpmsdata")  # function
async def getpmsdata(db: Session = Depends(services.get_database_session)):
    db_pmsdata = db.query(model.DummyPMSdata).all()
    if not db_pmsdata:
        raise HTTPException(
            status_code=400, detail="No data found on pms server")
    return db_pmsdata



