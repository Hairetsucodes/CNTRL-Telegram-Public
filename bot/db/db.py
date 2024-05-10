from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
import db.config as config
from db.models import User, PrivateMessages, ChatMessages

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

def add_message(id, username, chatId, message):
    db_session = SessionLocal()
    try:
        user = db_session.query(User).filter(User.id == id).first()
        if not user:
            add_user(username, id)
            db_session.commit()  # Ensure user addition is committed.

        if chatId == id:  # Assuming this logic is intended; revise if necessary.
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