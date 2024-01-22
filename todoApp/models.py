from sqlalchemy import Column, Integer, String
from database import engine
from main import Base

def create_tables():
    Base.metadata.create_all(engine)    