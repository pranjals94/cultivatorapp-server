from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ValidationError, validator

from fastapi import Depends, APIRouter, Request, Response, HTTPException

print("-----------------schema.py-----------------------------")


class person(BaseModel):
    # id: Optional[str]
    name: str
    phone_no: str
    email: str | None = None
    gender: str | None = None
    dob: datetime | None = None
    city: str | None = None

    class Config:
        orm_mode = True


class create_user(BaseModel):
    person_id: str
    username: str
    password: str
    role_id: str


class log_in(BaseModel):
    username: str
    password: str


class dummy_pms_data(BaseModel):
    name: str
    phone_no: str

    class Config:
        orm_mode = True

# //----------------pedantic Validator test----------------------------------------------
class test(BaseModel):
    name: str = ''
    role_id: int = 0
    test: str | None

    @validator('name', always=True)  # always= true means to check even if no data is received
    def Name(cls, v):
        if ' ' in v or v == '':
            # raise ValueError('Null Fields and Space not Allowed !')
            raise HTTPException(status_code=403, detail=f"Null Fields, Space and Roll id 0 not Allowed !")
        return v

    @validator('role_id', always=True)
    def Role_Id(cls, v):
        if v == 0:
            raise HTTPException(status_code=403, detail=f"Roll id 0 or null not Allowed !")
        return v

    class Config:
        orm_mode = True
        validate_all = True
