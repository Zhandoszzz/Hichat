from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database import get_db
from sqlalchemy.orm import Session
from app import utils, models, schemas, oauth2

router = APIRouter(
    tags=['Auth']
)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
async def login(user_info: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_info.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    if not utils.verify(user_info.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    access_token = oauth2.create_token(data={'username': user.username, 'id': user.id})
    return {"access_token": access_token, "token_type": "bearer"}
