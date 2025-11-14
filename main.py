from fastapi import FastAPI, Depends, HTTPException
  2 from datetime import date
  3 from pydantic import BaseModel
  4 from typing import Optional
  5
  6 from sqlalchemy import create_engine, Column, Integer, String, Date
  7 from sqlalchemy.ext.declarative import declarative_base
  8 from sqlalchemy.orm import sessionmaker, Session
