from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from ..database import get_db

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: schemas.UserLogin , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
        
    # create token
    # return token
    return {"token": "Example token"} 
