from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
import db.config as config
from db.models import User, PrivateMessages, ChatMessages, Chat, WordCounter, UserWordCount

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

def get_words(chatId):
    db_session = SessionLocal()
    try:
        words = db_session.query(WordCounter).filter(WordCounter.chatId == chatId).all()
        return [word.word for word in words]
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()


def word_results(chatId, userId):
    db_session = SessionLocal()
    try:
        words = db_session.query(UserWordCount).filter(UserWordCount.chatId == chatId, UserWordCount.userId == userId).all()
        return [f"{word.word}: {word.count}" for word in words]
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()

def add_word_count(chatId, word, userId):
    session = SessionLocal()
    try:
        word_count = session.query(WordCounter).filter(WordCounter.word == word, WordCounter.chatId == chatId).first()
        if not word_count:
            new_word_count = WordCounter(word=word, chatId=chatId)
            session.add(new_word_count)
            session.commit()
        user_word_count = session.query(UserWordCount).filter(UserWordCount.word == word, UserWordCount.userId == userId, UserWordCount.chatId == chatId).first()
        if not user_word_count:
            new_user_word_count = UserWordCount(word=word, userId=userId, count=1, chatId=chatId, username=session.query(User).filter(User.id == userId).first().username)
            session.add(new_user_word_count)
            session.commit()
        else:
            user_word_count.count += 1
            session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

def add_message(id, username, chatId, message: str):
    if chatId == None:
        return
    words = get_words(chatId)
    for word in words:
        if word in message:
            add_word_count(chatId, word, id)
            return
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
            return "Sorry there is no youtube link in this chat."
        return chat.lastYT
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()
        
def get_last_x_chat_messages(chatId, x):
    db_session = SessionLocal()
    try:
        """ return all X message from chatID  """
        messages = db_session.query(ChatMessages).filter(ChatMessages.chatId == chatId).all()[-x:]
        """ return message in a list make sure to but user name in front of message"""
        return [f"{message.username}: {message.message}" for message in messages]
      
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()
        
def check_b7(userId):
    db_session = SessionLocal()
    try:
        user = db_session.query(User).filter(User.id == userId).first()
        if user.blacklisted == 1:
            return True
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        db_session.rollback()
    finally:
        db_session.close()