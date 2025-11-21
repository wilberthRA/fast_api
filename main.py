from fastapi import FastAPI, Depends, HTTPException
from datetime import date
from pydantic import BaseModel
from typing import Optional
import bcrypt

from .data_base import SessionLocal, Base, engine
from sqlalchemy.orm import Session
from .Models.models import User, TareaDB 

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

app = FastAPI()

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

@app.post("/registrer/")
def registrer(user: UserCreate, db:Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(
            name= user.name, 
            email=user.email,
            password= hashed_password
            )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

class userLogin(BaseModel):
    email: str
    password: str

@app.post("/login/")
def login(user: userLogin, db:Session = Depends(get_db)):
    exist = db.query(User).filter(User.email == user.email).first()
    if exist is None:
        return {"status":"Error","message":"Password or email incorrect"}
    if bcrypt.checkpw(user.password.encode('utf-8'), exist.password):
        return {"status":"succes", "message":"Welcome"}
    else:
        return {"status":"Error","message":"Password incorrect"}

@app.get("/users/")
def read_users(skip: int = 0, Limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(Limit).all()
    return users

class taskCreate(BaseModel):
    titulo: str
    descripcion: str
    tiempo: date

@app.post("/tasks/")
def create_task(task: taskCreate, db: Session = Depends(get_db)):
    db_task = TareaDB(
            titulo = task.titulo,
            descripcion = task.descripcion,
            tiempo = task.tiempo
            )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks/")
def read_tasks(skip: int = 0, Limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(TareaDB).offset(skip).limit(Limit).all()
    return tasks

@app.get("/tasks/{id_task}")
def read_tasks(task_id: int, db:Session = Depends(get_db)):
    task = db.query(TareaDB).filter(TareaDB.id == task_id).first()
    if task is None:
        raise HTTPException(status_code = 404, details = "User not found")
    return task











