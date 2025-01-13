from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool =  True
    rating : Optional[int]= None

my_posts = [{"title": "post1 title", "content": "post1 content", "id": 1}, {"title": "post 2 title", "content": "post 2 content", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_post(id):
    return {"post detail": find_post(int(id))}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}