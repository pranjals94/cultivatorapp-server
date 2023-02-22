import sys

sys.path.append("..")

from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Header
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from datetime import datetime, timedelta
from jose import JWTError, jwt
from models import model
from schemas import schema
from fastapi.templating import Jinja2Templates

SECRET_KEY = "klhdjhgyguyrsouheor"
ALGORITHIM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

model.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="static")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not Authorised"}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(model.User).filter(model.User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)  # expire cookee in 60 mins
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHIM)


async def get_current_user(request: Request): #Request is global
    try:
        token = request.cookies.get("access_token")
        print("token", token)
        # print("cookie token received = ", token)
        if token is None:
            print("no Cookie token")
            return None
        playload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHIM])
        username: str = playload.get("sub")
        user_id: int = playload.get("id")
        if username is None or user_id is None:
            return None
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()


async def get_current_user_for_global_dependencies(request: Request):
    try:
        token = request.cookies.get("access_token")
        print("token", token)
        # print("cookie token received = ", token)
        if token is None:
            print("no Cookie token")
            raise HTTPException(status_code=401, detail="Sorry you are Unauthorized !")
            # return None
        playload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHIM])
        username: str = playload.get("sub")
        user_id: int = playload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Sorry User not Found!")
        request.state.user = {"username": username, "id": user_id}
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()


# Exceptions
def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could Not Validate Credintials",
        headers={"www-Authenticate": "Berarer"}
    )
    return credentials_exception


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"www-Authenticate": "Berarer"}
    )
    return token_exception_response


def check_logedin(request: Request):
    user = get_current_user(request)
    if user is None:
        # return {"reactNavigateTo": "/localhost:8000", "msg": "could not varify token/cookie"}
        raise HTTPException(status_code=401, detail="Sorry you are Unauthorized !")
    return user


@router.post("/login")
async def log_in_for_access_token(response: Response, login_credentials: schema.log_in,
                                  db: Session = Depends(get_db)):
    user = authenticate_user(login_credentials.username, login_credentials.password, db)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    response.set_cookie(key="access_token", value=token, httponly=False)
    return {"msg": "Log in Successful", "role": user.personRole.name, "username": user.username, "token": token}


@router.get("/logout")
async def logout(request: Request):
    response = templates.TemplateResponse("index.html", {"request": request, "msg": "Log out Successful"})
    response.delete_cookie(key="access_token")
    return response
