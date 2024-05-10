from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    blacklisted = Column(Integer, default=0)
    
class Messages(Base):
    __tablename__ = 'messages' 
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, nullable=False)
    message = Column(String(200), nullable=False)
    createdAt = Column(String(50), default=datetime.now())
    

    