from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str
    image_path: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class MessageCreate(BaseModel):
    owner_username: str
    receiver_username: str
    content: str


class MessageDisplay(BaseModel):
    id: int
    owner_id: int
    receiver_id: int
    content: str
    created_at: datetime

    owner: UserBase


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    id: Optional[int] = None
