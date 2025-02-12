from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings

import psycopg2
from psycopg2.extras import RealDictCursor

USERNAME = settings.database_username
PASSWORD = settings.database_password
HOSTNAME = settings.database_hostname
PORTNAME = settings.database_port
DATABASE_NAME = settings.database_name

SQLALCHEMY_DATABASE_URL = f'postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORTNAME}/{DATABASE_NAME}'

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