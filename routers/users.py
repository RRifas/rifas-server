from model.users_connection import userConnection
from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session, sessionmaker
from schema.user_schema import User
from fastapi import FastAPI, HTTPException
from fastapi import APIRouter 

conn = userConnection()

router= APIRouter()

SessionLocal=sessionmaker(bind=conn,expire_on_commit=False)
#Base.metadata.create_all(engine)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@router.post("/register")
def register_user(user: User, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password =get_hashed_password(user.password)

    new_user = User(username=user.username, email=user.email, password=encrypted_password )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message":"user created successfully"}
