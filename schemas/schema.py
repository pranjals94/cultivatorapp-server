from datetime import datetime, time
from typing import Optional
from pydantic import BaseModel, ValidationError, validator, Field

from fastapi import Depends, APIRouter, Request, Response, HTTPException

print("-----------------schema.py-----------------------------")

class filterSearch(BaseModel):
    startDate: datetime
    endDate: datetime

class exportexcel(BaseModel):
    persons: list = []


class add_visitor(BaseModel):
    orientation_id: int
    visitor_name: str = ''
    phone_no: int


class person(BaseModel):
    id: Optional[int]
    name: str = ''
    phone_no: int
    email: str | None = None
    gender: str | None = None
    dob: datetime | None = None
    city: str | None = None

    @validator('name', always=True)  # always= true means to check even if no data is received
    def Name(cls, v):
        if v is None or v == ' ' or v == '':
            # raise ValueError('Null Fields and Space not Allowed !')
            raise HTTPException(status_code=403, detail=f"Null Fields, Space and 0 not Allowed !")
        return v

    @validator('phone_no', always=True)  # always= true means to check even if no data is received
    def Phone_No(cls, v):
        if v is None or v == ' ' or v == '' or v > 9999999999999999999:
            # raise ValueError('Null Fields and Space not Allowed !')
            raise HTTPException(status_code=403, detail=f"Null Fields, Space, non valid phone No. and 0 not Allowed !")
        return v

    class Config:
        orm_mode = True
        validate_all = True


class create_user(BaseModel):
    person_id: str
    username: str
    password: str
    role_id: str


class log_in(BaseModel):
    username: str
    password: str


# middle_name: str | None = Field(regex="^[a-zA-Z ]+$", max_length=20)
class create_orientation(BaseModel):
    orientation_name: str = Field(regex="^[a-zA-Z0-9 ]+$", min_length=3, max_length=20)
    cultivator_id: int | None
    cultivator_assistant_id: int | None
    orienter_id: int | None
    orientation_start_date_time: datetime
    orientation_end_date_time: datetime
    venue: str = Field(regex="^[a-zA-Z0-9 ]+$", min_length=3, max_length=20)


# //-----------------assign cultivator to persons start------------
class active_cultivator(BaseModel):
    id: str
    name: str


class assign_cultivator_to_persons(BaseModel):
    cultivator: active_cultivator
    persons: list


# //-----------------assign cultivator to persons end--------------

class addparticipants(BaseModel):
    orientation: int
    visitors: list


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
            raise HTTPException(status_code=403, detail=f"Null Fields, Space and 0 not Allowed !")
        return v

    @validator('role_id', always=True)
    def Role_Id(cls, v):
        if v == 0:
            raise HTTPException(status_code=403, detail=f"Roll id 0 or null not Allowed !")
        return v

    class Config:
        orm_mode = True
        validate_all = True
