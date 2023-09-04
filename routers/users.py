from model.users_connection import userConnection
from schema.user_schema import User_data
from fastapi import APIRouter , HTTPException,Depends
from model.user_sesion import userConnection
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
import psycopg
from model.tokem import create_access_token, verify_token

conn = userConnection()

router= APIRouter()


@router.post("/register/", status_code=HTTP_201_CREATED)
def register(user_data: User_data):

    if not user_data:
        raise HTTPException(status_code=400, detail="Invalid request data")

    # Convert request data to dictionary
    data = user_data.dict()

    try:
        # Try to create a new rifa using the data
        rifa_id = conn.register(data)
    except psycopg.errors.UniqueViolation:
        # If a rifa with the same name already exists, raise a 409 Conflict error
        raise HTTPException(status_code=409, detail="User already exists")

    # Create response object with the new rifa's ID and name
    response_object = {
        "email": user_data.email,
      
    }

    return response_object

@router.post("/login/", status_code=HTTP_200_OK)
def login_route(email: str, password: str):
    # Llamamos a la función para autenticar al usuario
    user = conn.login_auth(email, password)
    
    if not user:
        # Si las credenciales son incorrectas, devolvemos un error 401 Unauthorized
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    
    access_token = create_access_token(user)
    return {"access_token": access_token}

@router.get("/profile/")
def get_profile(current_user: dict = Depends(verify_token)):
    return current_user  