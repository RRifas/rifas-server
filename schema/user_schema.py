from pydantic import BaseModel
from typing import Optional

class preorderschema(BaseModel):
    
    rifa_id:int
    tickets:int

class buyschema(BaseModel):
    transaction_id:int
    rifa_id:int
    tickets:int


class rifaschema(BaseModel):

    rifa_name:str
    goal:int
    price:int



    
    


