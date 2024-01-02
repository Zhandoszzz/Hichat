from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    username = Column(String, nullable=False, unique=True)
    image_path = Column(String)
    created_at = Column(TIMESTAMP(), server_default=text('now()'))
    password = Column(String, nullable=False)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(), server_default=text('now()'))

    owner = relationship("User", foreign_keys='Message.owner_id')