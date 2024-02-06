from typing import Optional
from sqlmodel import Field, SQLModel, create_engine,Session,select
from dotenv import load_dotenv,find_dotenv
from os import getenv


_:bool = load_dotenv(find_dotenv()) 

class Team(SQLModel,table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    headquarter: str

class Members(SQLModel,table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    age : Optional[int] = Field(default=None,index=True)
    team_id: Optional[int] = Field(foreign_key="team.id")


postgresql = getenv("POSTGRESS_URL") #todo table
engine = create_engine(postgresql,echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__": 
    create_db_and_tables() 

