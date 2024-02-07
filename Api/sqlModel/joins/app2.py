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

def create():
    with Session(engine) as session:
        team_3 = Team(name="FIA",headquarter="headquarter_1")
        
        session.add(team_3)
        session.commit()


def get_where_hero():
    with Session(engine) as session:
        statement = select(Members).where(Members.name == "Super Man")
        results = session.exec(statement)
        heros = results.all()
        print(heros)

def select_hero_by_join():
    with Session(engine) as session:
        statement = select(Members).join(Team)
        results = session.exec(statement)
        heros = results.all()
        print("Heros:",heros)   

def select_hero_by_join_where():
    with Session(engine) as session:
        statement = select(Members).join(Team).where(Team.name == "Justice League")
        results = session.exec(statement)
        heros = results.all()
        print("Heros:",heros)   

def select_Left_join():
    with Session(engine) as session:
        statement = select(Members).join(Team, isouter=True) #left join
        results = session.exec(statement)
        heros = results.all()
        print("Heros:", heros)                 

def select_right_join():
    with Session(engine) as session:
        statement = select(Members).join(Team, isouter=True) #right join
        results = session.exec(statement)
        heros = results.all()
        print("Heros:", heros)

def select_full_join():
    with Session(engine) as session:
        statement = select(Members).join(Team, isouter=True) #full join
        results = session.exec(statement)
        heros = results.all()
        print("Heros:", heros)



#remove data connections
def create_heroes():
    with Session(engine) as session:

        statement = select(Members).join(Team).where(Members.name == "Spider Man")
        results = session.exec(statement).first()

        results.team_id = None
        session.add(results)
        session.commit()
        
        print("No longer Preventer:", results)

        



if __name__ == "__main__": 
    create_heroes()
