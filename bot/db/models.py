from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    blacklisted = Column(Integer, default=0)
    
class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    userId = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(Text, nullable=False)  # Changed to Text type
    createdAt = Column(DateTime, default=datetime.now)  # Use DateTime type for actual date-time objects

    def __repr__(self):
        return f"<Message(id={self.id}, username='{self.username}', createdAt={self.createdAt})>"