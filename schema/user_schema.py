from pydantic import BaseModel, conint , constr
from typing import Optional



class buyschema(BaseModel):

    rifa_id:int
    tickets:conint (gt=0, le=1000)
    user_id = int
    type_transaction = str



class rifaschema(BaseModel):

    rifa_name:constr(max_length=30, strict=True)
    goal:conint (gt=0, le=1000)
    price:conint (gt=0, le=100)
    imagen:str
    description:constr(max_length=300, strict=True)

