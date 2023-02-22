import sys

sys.path.append("..")

from fastapi import Depends, APIRouter, Request, Response, HTTPException, File, UploadFile
from Modules import auth
from sqlalchemy.orm import Session
from models import model
from schemas import schema
import shutil

router = APIRouter(
    prefix="/globaldependencyexample",
    tags=["globalDependencyExample"],
    responses={401: {"user": "Not Authorised"}},
    dependencies=[Depends(auth.get_current_user_for_global_dependencies)]
)


@router.get("/")
async def serve_my_app(request: Request):
    user = request.state.user
    return {"user": user}


# //------------------file upload------------------------------
@router.post("/uploadfile")
async def serve_my_app(request: Request, file: UploadFile = File(...)):
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"FileName": file.filename}
