from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./smarter.db"
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:test@mysql/test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    #connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 
