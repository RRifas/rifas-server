from pydantic import BaseModel, conint , constr,EmailStr
from typing import Optional



class buyschema(BaseModel):

    id:int
    tickets:conint (gt=0, le=1000)
    user_id = int
    type_transaction = str



class rifaschema(BaseModel):

    name:constr(max_length=30, strict=True)
    goal:conint (gt=0, le=1000)
    price:conint (gt=0, le=100)
    description:constr(max_length=300, strict=True)
    imagen:constr(max_length=300)

class User_data (BaseModel):
    email : EmailStr
    first_name : constr(max_length=30, strict=True)
    last_name : constr(max_length=30, strict=True)
    phone : int
    address : constr(max_length=30, strict=True)
    gender : constr(max_length=30, strict=True)
    password : str

#class UserInDB(User):
  #  hashed_password: str

#class UserInLogin(User):
 #   password: str

