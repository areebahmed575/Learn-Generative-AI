from typing import Optional,List
from sqlmodel import Field, SQLModel, create_engine,Session,select,Relationship
from dotenv import load_dotenv,find_dotenv
from os import getenv

_:bool = load_dotenv(find_dotenv()) 

class HeroTeamLink(SQLModel, table=True):
    hero_id: Optional[int] = Field(default=None,foreign_key="members.id", primary_key=True)
    team_id: Optional[int] = Field(default=None,foreign_key="team.id", primary_key=True)

class Team(SQLModel,table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    headquarter: str
    members : List["Members"] = Relationship(back_populates = "teams", link_model=HeroTeamLink) 


class Members(SQLModel,table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    age : Optional[int] = Field(default=None,index=True)
    teams: List[Team] = Relationship(back_populates="members", link_model=HeroTeamLink) 


postgresql = getenv("POSTGRESS_URL") #todo table
engine = create_engine(postgresql,echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarter="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarter="Sister Margaret's Bar")

        hero_deadpond = Members(
            name="Deadpond",
            age=23,
            teams=[team_z_force, team_preventers],
        )
        hero_rusty_man = Members(
            name="Rusty-Man",
            age=48,
            teams=[team_preventers],
        )
        hero_spider_boy = Members(
            name="Spider-Boy", age=48, teams=[team_preventers]
        )
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()


def update():
    with Session(engine) as session:
        hero_spider_boy = session.exec(
            select(Members).where(Members.name == "Spider-Boy")
        ).one()
        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

        team_z_force.members.append(hero_spider_boy)
        session.add(team_z_force)
        session.commit()

        print("Updated Spider-Boy's Teams:", hero_spider_boy.teams)
        print("Z-Force heroes:", team_z_force.members)


#remove
def update_heros():
    with Session(engine) as session:
        hero_spider_boy = session.exec(
            select(Members).where(Members.name == "Spider-Boy")
        ).one()
        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()

        
        hero_spider_boy.teams.remove(team_z_force)
        session.add(team_z_force)
        session.commit()

        print("Reverted Z-Force's heroes:", team_z_force.members)
        print("Reverted Spider-Boy's teams:", hero_spider_boy.teams)      
        
        



if __name__ == "__main__": 
    update_heros()