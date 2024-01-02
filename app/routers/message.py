from fastapi import Depends, HTTPException, status, APIRouter
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, oauth2

router = APIRouter(
    tags=['Messages']
)


def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    owner = db.query(models.User).filter(models.User.username == message.owner_username).first()
    receiver = db.query(models.User).filter(models.User.username == message.receiver_username).first()

    if not owner or not receiver:
        raise HTTPException(status_code=404, detail="One or both users not found")

    new_message = models.Message(
        owner_id=owner.id,
        receiver_id=receiver.id,
        content=message.content,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def get_messages_between_users(owner_username: str, receiver_username: str, search: str, db: Session = Depends(get_db)):
    owner = db.query(models.User).filter(models.User.username == owner_username).first()
    receiver = db.query(models.User).filter(models.User.username == receiver_username).first()

    if not owner or not receiver:
        raise HTTPException(status_code=404, detail="One or both users not found")

    messages = db.query(models.Message).filter(
        ((models.Message.owner_id == owner.id) & (models.Message.receiver_id == receiver.id) |
         (models.Message.owner_id == receiver.id) & (models.Message.receiver_id == owner.id)) &
        (models.Message.content.contains(search))
    ).order_by(models.Message.created_at).all()
    return messages


@router.post("/chat/{username}", status_code=status.HTTP_201_CREATED, response_model=schemas.MessageDisplay)
async def send_message(username: str, content: str, current_user: str = Depends(oauth2.get_current_user),
                       db: Session = Depends(get_db)):
    # msg_dict = {
    #     "owner_username": current_user.username,
    #     "receiver_username": username,
    #     "content": content
    # }
    message = schemas.MessageCreate(
        owner_username=current_user.username,
        receiver_username=username,
        content=content
    )
    new_message = create_message(message, db)
    new_message.owner = username
    new_message.receiver = current_user.username
    return new_message


@router.get("/chat/{username}", response_model=List[schemas.MessageDisplay])
async def get_messages(username: str, current_user: str = Depends(oauth2.get_current_user),
                       db: Session = Depends(get_db), search: Optional[str] = ""):
    messages = get_messages_between_users(current_user.username, username, search, db)
    return messages
