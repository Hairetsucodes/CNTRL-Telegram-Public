from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(BIGINT, primary_key=True)
    username = Column(String(100), nullable=False)
    blacklisted = Column(Integer, default=0)


class PrivateMessages(Base):

    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    userId = Column(BIGINT, ForeignKey('users.id'), nullable=False)
    message = Column(Text, nullable=False)
    createdAt = Column(DateTime, default=datetime.now)


class ChatMessages(Base):
    __tablename__ = 'chatMessages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chatId = Column(BIGINT, nullable=False)
    username = Column(String(100), nullable=False)
    userId = Column(BIGINT, ForeignKey('users.id'), nullable=False)
    message = Column(Text, nullable=False)
    createdAt = Column(DateTime, default=datetime.now)


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    chatId = Column(BIGINT, nullable=False)
    lastYT = Column(Text, nullable=True)
    createdAt = Column(DateTime, default=datetime.now)


class UserWordCount(Base):
    __tablename__ = 'userWordCount'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(BIGINT, ForeignKey('users.id'), nullable=False)
    username = Column(String(100), nullable=False)
    chatId = Column(BIGINT, nullable=False)
    word = Column(String(50), nullable=False)
    count = Column(Integer, nullable=False)
    createdAt = Column(DateTime, default=datetime.now)

class WordCounter(Base):
    __tablename__ = 'wordCounter'
    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(50), nullable=False)
    chatId = Column(BIGINT, nullable=True)
    createdAt = Column(DateTime, default=datetime.now)
