from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from db import config
from db.models import User, Messages

engine = create_engine(config.DATABASE_URI, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


def add_user(name, telegram_id):
    db_session = SessionLocal()
    new_user = User(name=name, telegram_id=telegram_id)
    db_session.add(new_user)
    db_session.commit()
    db_session.close()

def add_message(user_id, username, message, createdAt):
    db_session = SessionLocal()
    if not db_session.query(User).filter(User.id == user_id).first():
        add_user(username=username, id=User.id)
    new_message = Messages(userId=user_id, username=username, message=message, createdAt=createdAt)
    db_session.add(new_message)
    db_session.commit()
    db_session.close()