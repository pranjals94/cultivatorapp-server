from fastapi import Depends, APIRouter, Request, Response, HTTPException
from fastapi.templating import Jinja2Templates
from models import model
from Common import services
from sqlalchemy.orm import Session
from schemas import schema

templates = Jinja2Templates(directory="static")
router = APIRouter()


# catch all get request in path "/app/***" ----------------------------------------------------
@router.get("/app/{rest_of_path:path}")
async def serve_my_app(request: Request, rest_of_path: str):
    return templates.TemplateResponse("index.html", {"request": request, "msg": "Dont send request via addressbar"})


# -----------------------------------------------------------------------------


@router.get("/app")
async def serve_my_app(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "msg": "Dont send request via addressbar"})


# --------------------------pydentic validator test-------------------------------------------------------------
@router.post("/testValidator")
async def serve_my_app(test: schema.test, request: Request):
    return {"test": test}


@router.post("/testalchemy")
async def test_alchemy(test: schema.test, db: Session = Depends(services.get_database_session)):
    # query = select([model.User.username]).where(model.User.id.in_([15]))
    # users = auth.engine.execute(query).all()
    # tempUsers = db.query(model.User.username, model.User.id).where(model.User.id.in_([19])).all()
    tempUsers = db.query(model.Role.id).all()
    users: list = [{"hi": "hello", "arrey": [1, 2, 5, 6]}]
    for user in tempUsers:
        result = user.id
        users.append(result)
    return {"users": users, "object": test}


# //-----dependency test ----------------------------------------
dummy = "true"


async def test1():
    if dummy != 'tgrue':
        raise HTTPException(status_code=401, detail="Sorry you are Unauthorized !")
    return "true"


@router.get("/dependencytest")
async def test_alchemy(temp: str = Depends(test1)):
    return temp
