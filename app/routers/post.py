from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. database import get_db
from .. import models, schemas, oauth2

router = APIRouter(prefix="/posts", tags=['Posts'])

# all posts
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user),
                limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isOuter=True).group_by(models.Post.id)

    # display posts owned by current user
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id)

    return posts

# single post
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
 
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id:{id} not found.")

    # Get particular post of current user. Cannot get posts from other user if enabled.
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action.")
    
    return post

# create post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id= current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# delete post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # connection.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id:{id} not found.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """, 
    #                (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    # connection.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
   
    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id:{id} not found.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")
    
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