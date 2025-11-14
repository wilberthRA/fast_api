from fastapi import FastAPI, Depends, HTTPException
from datetime import date
from pydantic import BaseModel
from typing import Optional

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

DATABASE_URL = "sqlite:///tareas.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

class TareaDB(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    descripcion = Column(String)
    tiempo = Column(Date)

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name: str
    email: str

@app.post("/users/")
def create_user(user: UserCreate, db: Session=Depends(get_db)):
    db_user = User(name=user.name, email= user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/")
def read_users(skip: int = 0, Limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(Limit).all()
    return users

@app.get("/users/{user_id}")
def read_users(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code = 404, details = "User not found")
    return user
 
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

@app.post("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code = 404, details = "User not found")
    db_user.name = user.name if user.name is not None else db_user.name
    db_user.email = user.email if user.email is not None else db_user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code = 404, details = "User not found")

    db.delete(db_user)
    db.commit()
    return db_user
