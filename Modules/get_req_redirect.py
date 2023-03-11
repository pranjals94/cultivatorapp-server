
from fastapi import Depends, APIRouter, Request, Response, HTTPException
from fastapi.templating import Jinja2Templates


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


