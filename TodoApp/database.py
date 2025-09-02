from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# sqlite setup
# SQLALCHEMY_DATABASE_URL = 'sqlite:///todosapp.db'
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# protgres setup - test password, welps
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Gordon123!@localhost:5432/TodoApplicationDatabase'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 