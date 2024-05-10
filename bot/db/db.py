from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
import db.config as config
from db.models import User, PrivateMessages, ChatMessages, Chat

engine = create_engine(config.DATABASE_URI, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)

def add_user(username, id):
    db_session = SessionLocal()
    try:
        new_user = User(username=username, id=id)
        db_session.add(new_user)
        db_session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()

def add_message(id, username, chatId, message: str):
    db_session = SessionLocal()
    try:
        user = db_session.query(User).filter(User.id == id).first()
        if not user:
            add_user(username, id)
            db_session.commit()  
        if "youtube.com" in message:
            add_youtube(message, chatId)
        if chatId != id: 
            new_message = ChatMessages(username=username, userId=id, chatId=chatId, message=message)
        else:
            new_message = PrivateMessages(username=username, userId=id, message=message)

        db_session.add(new_message)
        db_session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()
        
        
create_tables()
        
def add_youtube(message, chatId):
    db_session = SessionLocal()
    try:
        chat = db_session.query(Chat).filter(Chat.chatId == chatId).first()
        if not chat:
            new_chat = Chat(chatId=chatId, lastYT=message)
            db_session.add(new_chat)
            db_session.commit()
        else:
            chat.lastYT = message
            db_session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()
        
def last_youtube(chatId):
    db_session = SessionLocal()
    try:
        chat = db_session.query(Chat).filter(Chat.chatId == chatId).first()
        if not chat:
            return "https://www.youtube.com/watch?v=Kz9Mx6XJN7A"
        return chat.lastYT
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()