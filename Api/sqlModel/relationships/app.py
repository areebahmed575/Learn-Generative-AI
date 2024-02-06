from typing import Optional,List
from sqlmodel import Field, SQLModel, create_engine,Session,select,Relationship
from dotenv import load_dotenv,find_dotenv
from os import getenv


_:bool = load_dotenv(find_dotenv()) 

class Team(SQLModel,table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    headquarter: str
    members : List["Members"] = Relationship(back_populates = "team") #many members in one team


class Members(SQLModel,table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    age : Optional[int] = Field(default=None,index=True)
    team_id: Optional[int] = Field(foreign_key="team.id")
    team : Optional[Team] = Relationship(back_populates = "members") #one team for many members


postgresql = getenv("POSTGRESS_URL") #todo table
engine = create_engine(postgresql,echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create():
    with Session(engine) as session:
        team_fighter = Team(name = "Air Fighters" , headquarter= "New York")
        team_moon = Team(name = "Moon Fighters" ,headquarter= "Moon")

        hero_1 = Members(name="Areeb Ahmed", age="23",team=team_fighter)
        hero_2 = Members(name="Ali Khan", age="23",team=team_moon)

        session.add_all([team_fighter,team_moon,hero_1,hero_2])
        session.commit()


def create_members_in_team():
    with Session(engine) as session:
       hero_3 = Members(name="Black Panther", age="23")
       hero_4 = Members(name="Aqua Man", age="23")

       team_earth = Team(name = "Earth Fighters", headquarter= "Earth",members=[hero_3,hero_4]) 
       session.add(team_earth)
       session.commit()


def update():
    with Session(engine) as session:
        stat = select(Team).where(Team.name == "Air Fighters") 
        team = session.exec(stat).first()
        stat2 = select(Members).where(Members.name == "Spider Man")
        hero = session.exec(stat2).first()
        hero.team = team
        session.commit()






if __name__ == "__main__": 
    create_members_in_team()

        
