from dotenv import load_dotenv
import os

from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post

models.Base.metadata.create_all(engine)

app = FastAPI()

load_dotenv()
PASSWORD = os.getenv("PASSWORD")

try:
    connection = psycopg2.connect(host='localhost', database='smapi', user='postgres', 
                                  password=PASSWORD, cursor_factory=RealDictCursor)
    cursor = connection.cursor()
    print('Connection to db sucessful!')
except Exception as error:
    print('Connection to db failed.')
    print("Error: ",error)

app.include_router(post.router)
# app.include_router(post.router)

# home
@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id:{id} not found.")
    
    return user
