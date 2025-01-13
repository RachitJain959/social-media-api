from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool =  True
    rating : Optional[int]= None

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/posts")
def get_posts():
    return {"data": "These are all your posts."}

@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post)
    return {"data": "new post"}