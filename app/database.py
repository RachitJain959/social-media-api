from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()
USERNAME = os.getenv("MYUSERNAME")
PASSWORD = os.getenv("PASSWORD")
IP_ADDRESS = os.getenv("IP_ADDRESS")
DATABASE_NAME = os.getenv("DATABASE_NAME")

SQLALCHEMY_DATABASE_URL = f'postgresql://{USERNAME}:{PASSWORD}@{IP_ADDRESS}/{DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Session to db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# connect to raw postgres
# try:
#     connection = psycopg2.connect(host='localhost', database='smapi', user='postgres', 
#                                   password=PASSWORD, cursor_factory=RealDictCursor)
#     cursor = connection.cursor()
#     print('Connection to db sucessful!')
# except Exception as error:
#     print('Connection to db failed.')
#     print("Error: ",error)