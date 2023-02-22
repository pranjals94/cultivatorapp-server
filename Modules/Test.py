from fastapi import Path, Query, Body
from enum import Enum
from pydantic import BaseModel
from database import SessionLocal, engine
from models import model
from schemas import schema
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from starlette.responses import JSONResponse

app = FastAPI()

# --------------allow cors--------------------------
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------------------------------------------


class option(BaseModel):
    gender: str
    telephone: int


class User(BaseModel):
    id: int
    name: str
    age: int
    dept: str
    # optional, can be string or null, default value is "testCity"
    city: str | None = "testCity"
    options: option


model.Base.metadata.create_all(bind=engine)


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/getPost")
async def post(data: User):
    print(data.options.telephone)
    return data


@app.get("/")  # function
async def read_root():
    return {"Hello": "World"}

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: str | None = None, r: str | None = None):
#     return {"item_id": item_id, "q": q, "r": r}


def printinfo(arg1, *vartuple):
    print("Output is: ")
    print(arg1)
    for var in vartuple:
        print(var)
    return


@app.get("/test1")  # function
async def test1():
    # Now you can call printinfo function
    printinfo(10)
    printinfo(70, {"price": 60, "discount": 78}, 50)
    list = [1, 2, "abc", 123.67]
    return {"msg": 'Ok', "list": list}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")  # function
async def test2(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/test2")  # function
async def test2(arg):
    for var in arg:
        print(var)
    return

# for querry parameters validations use Query()
# for path parameters validation use Path()


@app.get("/items/{item_id}")
async def read_items(item_id: int = Path(title="The ID of the item to get", ge=1, le=10), q: str | None = Query(default="DefalutValue", max_length=5)):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.get("/goods/{good_id}")
async def read_items(*, good_id: int = Path(title="The ID of the item to get"), q: str):
    results = {"good_id": good_id}
    if q:
        results.update({"q": q})
    return results

# ----------------------------------------------------------------------------------------------------------


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User1(BaseModel):
    username: str
    full_name: str | None = None


@app.post("/itms/{item_id}")
async def update_item(item_id: int,  item: Item, user: User1, importance: int = Body(gt=1), txt: str = Body()):
    print(item.name)
    results = {"item_id": item_id, "item": item,
               "user": user, "importance": importance,
               "text": txt
               }
    return results

# use embed= true for a single body parameter


@app.post("/singleBodyParameter")
async def update_item(item: Item = Body(embed=True)):
    results = {"item": item}
    return results


@app.get("/movie")
async def read_movies(db: Session = Depends(get_database_session)):
    records = db.query(model.Movie).all()
    return {"data": records}


@app.get("/deletemovie/{id}")
async def delete_movie(id: int, db: Session = Depends(get_database_session)):
    movie = db.query(model.Movie).get(id)
    if movie:
        db.delete(movie)
        db.commit()
        return JSONResponse(status_code=200, content={
            "status_code": 200,
            "message": "success",
            "movie": None
        })
    return {"msg": "no movie found"}

# --------------------------------------------------------------------


@app.post("/createitem")
def create_item(user: schema.UserCreate, db: Session = Depends(get_database_session)):
    db_item = model.Item(
        title="hi", description="item Description")
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# ------------------------------------------------------------------------------------------------------


@app.get("/createitemwithrelation")
def create_item_with_relation(user: schema.UserCreate, db: Session = Depends(get_database_session)):
    db_user = model.User(
        title="hi", description="item Description")
    db_item = model.Item(
        title="relationshipitem", description="item Description relationship")
# --------------------------------------------------------------------------------------------------------


@app.get("/getuser")
def get_user(db: Session = Depends(get_database_session)):
    """
        multiline
        comment
    """
    '''
        again
        multiline
        comment
    '''
    item = db.get(model.Item, 1)
    print(item.dict())
    return "ok"


@app.post("/createuser/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_database_session)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/deleteuser/", response_model=schema.User)
def del_user(user: schema.UserCreate, db: Session = Depends(get_database_session)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        crud.delete_user(db=db, user=user)
    raise HTTPException(status_code=400, detail="Email not found")

# --------------------------------------------------------------------------------------------------------------


@app.get("/getpagination")
def get_items(db: Session = Depends(get_database_session)):
    return db.query(model.Movie).offset(2).limit(5).all()


# ----------------------------react pings from here--------------------------------------------------------------------
@app.get("/listmovies")
async def read_movies(db: Session = Depends(get_database_session)):
    records = db.query(model.Movie).all()
    return {"data": records}


@app.post("/createmovie")
async def create_movie(movie: schema.Movie, db: Session = Depends(get_database_session)):
    print(movie.name)
    db_movie = db.query(model.Movie).filter(
        model.Movie.name == movie.name).first()
    if db_movie:
        raise HTTPException(status_code=400, detail="Movie Name Already Exist")
    db_movie = model.Movie(**movie.dict())  # maps the data
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


@app.get("/deletemovie/{movie_id}")
async def delete_movie(movie_id: int, db: Session = Depends(get_database_session)):
    print("movie id", movie_id)
    db_movie = db.query(model.Movie).filter(model.Movie.id == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=400, detail="Movie does not Exist")
    db.delete(db_movie)
    db.commit()
    records = db.query(model.Movie).all()
    return {"msg": "Movie with Id {movie_id} Deleted", "data": records}


@app.post("/update")
async def delete_movie(movie: schema.Movie, db: Session = Depends(get_database_session)):
    print("movie name", movie.id)
    db_movie = db.get(model.Movie, movie.id)
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie Not Found")
    movie_data = movie.dict(exclude_unset=True)
    for key, value in movie_data.items():
        setattr(db_movie, key, value)
    db.add(db_movie)
    db.commit()
    records = db.query(model.Movie).all()
    return {"msg": "updated ok", "data": records}
