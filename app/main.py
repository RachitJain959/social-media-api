from dotenv import load_dotenv
import os

from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(engine)

app = FastAPI()


load_dotenv()
PASSWORD = os.getenv("PASSWORD")

class Post(BaseModel):
    title: str
    content: str
    published: bool =  True
    rating : Optional[int]= None

try:
    connection = psycopg2.connect(host='localhost', database='smapi', user='postgres', 
                                  password=PASSWORD, cursor_factory=RealDictCursor)
    cursor = connection.cursor()
    print('Connection to db sucessful!')
except Exception as error:
    print('Connection to db failed.')
    print("Error: ",error)



my_posts = [{"title": "post1 title", "content": "post1 content", "id": 1}, {"title": "post 2 title", "content": "post 2 content", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
        
def find_index(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i

# home
@app.get("/")
async def root():
    return {"message": "Hello world"}

# all posts
@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()

    return {"data": posts}

# single post
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id:{id} not found.")

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": f"post with id:{id} not found."}
    return {"post detail": post}

# create post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                    (post.title, post.content, post.published))

    new_post = cursor.fetchone()
    connection.commit()

    return {"data": new_post}

# delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    connection.commit()

    if deleted_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id:{id} not found.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """, 
                   (post.title, post.content, post.published, str(id)))
    
    updated_post = cursor.fetchone()
    connection.commit()

    if updated_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id:{id} not found.")
    
    return {"data": updated_post}

@app.get("/test")
def test_post(db: Session = Depends(get_db)):
    return {"status": "Success"}