from fastapi import APIRouter
import psycopg
from fastapi import HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from model.users_connection import userConnection
from schema.user_schema import rifaschema, buyschema
from config.init import create_tables

router = APIRouter()

conn = userConnection()


@router.get("/", status_code=HTTP_200_OK)
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
            "id": rifa[0],
            "name": rifa[1],
            "description": rifa[2],
            "price": rifa[3],
            "goal": rifa[4],
            "tickets_sold": rifa[5] or 0,
        }

        # Calculate the rifas status (percentage of tickets sold)
        if rifa_dict["id"]:
            rifa_dict["status"] = (
                str(rifa_dict["tickets_sold"] / rifa_dict["goal"] * 100) + "%"
            )
            # Add the rifa dictionary to the list of rifas items
            rifas_items.append(rifa_dict)

    # Return the list
    return rifas_items


@router.post("/api/create", status_code=HTTP_201_CREATED)
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
        "id": rifa_id[0],
        "name": rifa_id[1],
    }

    return response_object


@router.put("/api/update/{id}", status_code=HTTP_204_NO_CONTENT)
def update(rifa_data: rifaschema, id: int):
    # A dictionary is created with the id received in the URL
    id2 = {"id": id}
    # The corresponding rifa for the id is searched for in the database
    rifa = conn.get_rifa_by_id(id2)

    # If no valid data is received, an HTTP 422 exception is raised
    if rifa is None:
        raise HTTPException(status_code=404, detail="rifa not found")

    # If no valid data is received, an HTTP 422 exception is raised
    if not rifa_data:
        raise HTTPException(status_code=422, detail="Invalid data")
    # The received rifa information is converted into a dictionary
    rifa_data_dict = rifa_data.dict()
    # The id received in the URL is added to the rifa dictionary
    rifa_data_dict.update({"id": id})
    # The rifa information is updated in the database
    conn.modify_rifa(rifa_data_dict)


@router.delete("/api/delete/{id}", status_code=HTTP_204_NO_CONTENT)
def delete(id: int):
    # Create a dictionary with the id received in the URL
    id = {"id": id}

    # Find the rifa corresponding to the id in the database
    rifa = conn.get_rifa_by_id(id)
    # If the rifa is not found, raise an HTTP 404 exception
    if rifa is None:
        raise HTTPException(status_code=404, detail="Rifa not found")

    # Delete the rifa from the database
    conn.delete_rifa(id)


@router.post("/api/preorder", status_code=HTTP_201_CREATED)
def preorder_tickets(buy_data: buyschema):
    rifa_id = conn.get_rifa_by_id({"id": buy_data.rifa_id})
    if not rifa_id:
        raise HTTPException(status_code=404, detail="Rifa not found")

    available_tickets = conn.get_available_tickets(buy_data.dict())
    if not available_tickets:
        raise HTTPException(status_code=400, detail="Ticket not available")

    return available_tickets


# Define the endpoint to buy a ticket
@router.post("/api/buy", status_code=HTTP_201_CREATED)
def buy_tickets(buy_data: buyschema):
    data = buy_data.dict()
    rifa = conn.get_rifa_by_id({"id": data["id"]})

    if rifa == None:
        raise HTTPException(status_code=404, detail="Rifa not found")

    rifa = conn.get_available_tickets(data)
    if not isinstance(rifa, dict):
        raise HTTPException(status_code=400, detail="Ticket not available")

    # Create a transaction record in the database
    transaction_id = conn.create_transaction(
        {
            "id": data["id"],
            "total_price": rifa["total_price"],
            "tickets": data["tickets"],
        }
    )
    if not isinstance(transaction_id, int):
        raise HTTPException(status_code=400, detail="Error creating rifa")
    # transaction_id=int
    return "gracias por tu compra che"


# TODO: remove endpoint after db is stable
@router.get("/api/create-tables", status_code=HTTP_200_OK)
def create_tables_endpoint():
    create_tables()
    return "tables updated"
