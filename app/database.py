from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from .config import DATABASE_UNAME, DATABASE_PASS, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
#SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_UNAME}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()