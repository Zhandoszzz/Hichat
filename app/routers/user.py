from fastapi import Depends, HTTPException, status, Response, APIRouter
from app.database import get_db
from sqlalchemy.orm import Session
from app import utils, models, schemas, oauth2

router = APIRouter(
    tags=['Users']
)

#
@router.get("/")
async def get_users():
    return "hello"


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserBase)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        user.password = utils.hash_password(user.password)
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    elif user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='user already exists')


@router.get("/{id}", response_model=schemas.UserBase)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found')
    return user


@router.delete("/{id}")
async def delete_user(id: int, db: Session = Depends(get_db),
                      current_user: str = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found')
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized')
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.UserBase)
async def update_user(id: int, updated_user: schemas.UserBase, db: Session = Depends(get_db),
                      current_user: str = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="user not found")
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized')
    user_query.update(updated_user.model_dump(), synchronize_session=False)
    db.commit()

    return user_query.first()
