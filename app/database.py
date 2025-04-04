from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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
