from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from db import config
from db.models import User

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
