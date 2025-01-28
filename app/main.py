from dotenv import load_dotenv
import os

from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user

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
app.include_router(user.router)

# home
@app.get("/")
async def root():
    return {"message": "Hello world"}


