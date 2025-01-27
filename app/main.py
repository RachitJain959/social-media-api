from typing import List
from dotenv import load_dotenv
import os

from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

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

# home
@app.get("/")
async def root():
    return {"message": "Hello world"}

# all posts
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()
    return posts

# single post
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id:{id} not found.")

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"error": f"post with id:{id} not found."}
    return post

# create post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                 (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # connection.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # connection.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id:{id} not found.")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """, 
    #                (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    # connection.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
   
    # print(type(post)) 
    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id:{id} not found.")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
# def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    # Get the existing SQLAlchemy post
    db_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = db_query.first()

    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"Post with id:{id} not found.")
    
    # Update the SQLAlchemy post instance with data from Pydantic model
    for key, value in post.dict(exclude_unset=True).items():  # Use dict() here
        setattr(db_post, key, value)  # Set the attribute on the SQLAlchemy instance

    db.commit()
    return {"data": db_query.first()}

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user