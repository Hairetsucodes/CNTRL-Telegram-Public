from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
import db.config as config
from db.models import User, Messages

engine = create_engine(config.DATABASE_URI, echo=True)

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

def add_message(id, username, message):
    db_session = SessionLocal()
    new_message = Messages(userId=id, username=username, message=message)
    db_session.add(new_message)
    db_session.commit()
    db_session.close()
    
    
    