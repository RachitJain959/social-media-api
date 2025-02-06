from dotenv import load_dotenv
import os

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(engine)

app = FastAPI()

load_dotenv()
PASSWORD = os.getenv("PASSWORD")


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# home
@app.get("/")
async def root():
    return {"message": "Hello world"}


