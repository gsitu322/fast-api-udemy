from fastapi import FastAPI, Depends

from database import SessionLocal
from database import engine

from typing import Annotated
from sqlalchemy.orm import Session
import models
from models import Todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(Todos).all()