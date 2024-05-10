from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    telegram_id = Column(Integer, nullable=False)
    blacklisted = Column(Integer, nullable=False)
    
class Messages(Base):
    __tablename__ = 'messages' 
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    message = Column(String(200), nullable=False)
    createdAt = Column(String(50), nullable=False)
    

    