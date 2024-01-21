from sqlalchemy import Column, Integer, String
from database import Base,engine

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)


def create_tables():
    Base.metadata.create_all(engine)    