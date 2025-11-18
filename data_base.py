from sqlalchemy import create_engine, Column, Integer, String, Date 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URl = "sqlite:///tareas.db"

engine = create_engine(DATABASE_URl,connect_args = {"check_same_thread": False})

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

