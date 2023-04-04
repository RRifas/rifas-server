import json
import re
import psycopg
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from model.users_connection import userConnection
from schema.user_schema import rifaschema,buyschema

# Creating a FastAPI instance
app = FastAPI()

# Creating a userConnection instance to connect to the database
conn = userConnection()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=HTTP_200_OK)
def get_rifas():
    # Retrieve all rifas from the database and return their data in JSON format

    # Initialize an empty list to store rifas items
    rifas_items = []

    # Retrieve all rifas from the database
    rifas = conn.read_all()

    # Iterate over each rifa in the list of retrieved rifas
    for rifa in rifas:
        # Create a dictionary with the rifas data
        rifa_dict = {
            'name': rifa[0],
            'description': rifa[1],
            'price': rifa[2],
            'goal': rifa[3],
            'tickets_sold': rifa[4] or 0
        }

        # Calculate the rifas status (percentage of tickets sold)
        rifa_dict['status'] = str(
            rifa_dict['tickets_sold'] / rifa_dict['goal'] * 100) + '%'

        # Add the rifa dictionary to the list of rifas items
        rifas_items.append(rifa_dict)

    # Convert the list of rifas items to JSON format with indentation for readability
    final = json.dumps(rifas_items)

    # Return the JSON string
    return final


@app.post("/api/create", status_code=HTTP_201_CREATED)
def create_rifas(rifa_data: rifaschema):
    # Check if request data is valid
    if not rifa_data:
        raise HTTPException(status_code=400, detail="Invalid request data")

    # Convert request data to dictionary
    data = rifa_data.dict()

    try:
        # Try to create a new rifa using the data
        rifa_id = conn.create_a_rifa(data)
    except psycopg.errors.UniqueViolation:
        # If a rifa with the same name already exists, raise a 409 Conflict error
        raise HTTPException(status_code=409, detail="Rifa already exists")

    # Create response object with the new rifa's ID and name
    response_object = {
        "rifa_id": rifa_id[0],
        "rifa_name": rifa_id[1],
    }

    return response_object


@app.put("/api/update/{id}", status_code=HTTP_204_NO_CONTENT)
def update(rifa_data: rifaschema, id: int):
    # A dictionary is created with the id received in the URL
    id2 = {'id': id}
    # The corresponding rifa for the id is searched for in the database
    rifa = conn.get_rifa_by_id(id2)

    # If no valid data is received, an HTTP 422 exception is raised
    if rifa is None:
        raise HTTPException(status_code=404, detail='rifa not found')

    # If no valid data is received, an HTTP 422 exception is raised
    if not rifa_data:
        raise HTTPException(status_code=422, detail='Invalid data')
    # The received rifa information is converted into a dictionary
    rifa_data_dict = rifa_data.dict()
    # The id received in the URL is added to the rifa dictionary
    rifa_data_dict.update({'rifa_id': id})
    # The rifa information is updated in the database
    conn.modify_rifa(rifa_data_dict)


@app.delete("/api/delete/{id}", status_code=HTTP_204_NO_CONTENT)
def delete(id: int):
    # Create a dictionary with the id received in the URL
    id = {'id': id}

    # Find the rifa corresponding to the id in the database
    rifa = conn.get_rifa_by_id(id)
    # If the rifa is not found, raise an HTTP 404 exception
    if rifa is None:
        raise HTTPException(status_code=404, detail="Rifa not found")

    # Delete the rifa from the database
    conn.delete_rifa(id)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={'message': exc.detail}
    )



@app.post("/api/preorder", status_code=HTTP_201_CREATED)
def preorder_tickets(buy_data: buyschema):
    rifa_id = conn.get_rifa_by_id({'id': buy_data.rifa_id})
    if not rifa_id:
        raise HTTPException(status_code=404, detail="Rifa not found")

    available_tickets = conn.get_available_tickets(buy_data.dict())
    if not available_tickets:
        raise HTTPException(status_code=400, detail="Ticket not available")

    return available_tickets


# Define the endpoint to buy a ticket
@app.post("/api/buy", status_code=HTTP_201_CREATED)
def buy_tickets(buy_data: buyschema):

    data=buy_data.dict()
    rifa=conn.get_rifa_by_id({'id':data['rifa_id']})

    if rifa== None:
        raise HTTPException(status_code=404, detail="Rifa not found")

    rifa=conn.get_available_tickets(data)
    if not isinstance(rifa, dict):
        raise HTTPException(status_code=400, detail="Ticket not available")

    # Create a transaction record in the database
    transaction_id = conn.create_transaction({"rifa_id":data['rifa_id'],"total_price":rifa['total_price'],"tickets":data['tickets']})
    if not isinstance(transaction_id, int):
        raise HTTPException(status_code=400, detail="Error creating rifa")
    #transaction_id=int
    return "gracias por tu compra che"

