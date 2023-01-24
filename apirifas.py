
from fastapi import FastAPI, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from model.users_connection import userConnection
import json
from schema.user_schema import buyschema, rifaschema, preorderschema

app = FastAPI( )
conn=userConnection

@app.get("/", status_code=HTTP_200_OK)
def root():
    


    item=[]
    data= conn().read_all()
    

    dict1={}
    key_list = ['descripcion', 'goal', 'id','tickets_vendidos']
    
    

    for i in data:
        if len(i)==3:
            dict_from_list = dict(zip(key_list, i))
            dict_from_list ['status']='0%'
            item.append(dict_from_list)
            final = json.dumps(item, indent=1)  

        else:

            dict_from_list = dict(zip(key_list, i))
            dict_from_list ['status']=str(dict_from_list['tickets_vendidos']/dict_from_list['goal']*100)+'%'
            item.append(dict_from_list)
            final = json.dumps(item, indent=1)  
    return  final

@app.post("/api/insert",status_code=HTTP_201_CREATED)
def insert(buy_data:preorderschema):
    data=buy_data.dict()
    conn().preorder_a_ticket(data)

    return Response (status_code=HTTP_201_CREATED)

@app.post("/api/buy",status_code=HTTP_201_CREATED)
def insert(buy_data:buyschema):
    data=buy_data.dict()
    conn().buy_a_ticket(data)

    return Response (status_code=HTTP_201_CREATED)
    
@app.delete("/api/cancel/{id}",status_code=HTTP_204_NO_CONTENT)
def detele(id:str):
    conn().cancel_ticket(id)

    return Response (status_code=HTTP_204_NO_CONTENT)

@app.post("/api/create",status_code=HTTP_201_CREATED)
def insert(rifa_data:rifaschema):
    data=rifa_data.dict()
    conn().create_a_rifa(data)

    return Response (status_code=HTTP_201_CREATED)

@app.put("/api/update/{id}",status_code=HTTP_204_NO_CONTENT)
def update(rifa_data:rifaschema,id:str):
    data=rifa_data.dict()
    data['rifa_id']=id

    conn().modify_rifa(data)

    return Response (status_code=HTTP_204_NO_CONTENT)




@app.delete("/api/delete/{id}",status_code=HTTP_204_NO_CONTENT)
def detele(id:str):
    conn().delete_rifa(id)

    return Response (status_code=HTTP_204_NO_CONTENT)


