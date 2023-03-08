from models import model
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from database import engine
from starlette.staticfiles import StaticFiles

# ------------------------router imports-------------------
from Modules import auth
from Modules import application
from Modules import get_req_redirect
from Modules import globalDependenctExample
from Modules import reception
from Modules import admin
from Modules import cultivator

print("----------main.py file serving-------------------------")
model.Base.metadata.create_all(bind=engine)  # create database


app = FastAPI()


# --------------allow cors--------------------------
origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(application.router)
app.include_router(get_req_redirect.router)
app.include_router(globalDependenctExample.router)
app.include_router(reception.router)
app.include_router(admin.router)
app.include_router(cultivator.router)
app.mount('/', StaticFiles(directory="static", html=True), name="static")



