from fastapi import FastAPI,Depends,HTTPException,Query
from sqlmodel import Field, SQLModel, create_engine,Session,select,Relationship
from typing import Annotated



class TeamBase(SQLModel):
    name:str = Field(index=True)
    headquarter : str

class Team(TeamBase,table=True):
    id:int|None =Field(default=None,primary_key=True)
    heroes:list["Hero"] = Relationship(back_populates="team")
    

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id:int
    
class TeamUpdate(SQLModel):
    name : str | None = None
    headquarter : str | None = None


# class TeamResponseWithHeroes(TeamResponse):
#      hero : HeroResponse
#      #hero : list[HeroResponse] = []
    

class HeroBase(SQLModel):
    name:str = Field(index=True)
    secret_name:str
    team_id:int|None = Field(default=None, foreign_key="team.id")

class Hero(HeroBase,table=True):
    id:int|None =Field(default=None,primary_key=True)
    description:str|None=None
    
    team:Team = Relationship(back_populates="heroes")
    
class HeroCreate(HeroBase):
    description:str|None=None
   


class HeroResponse(HeroBase):
    id:int
    description:str|None=None
    

class HeroUpdate(SQLModel):
    name:str|None=None
    secret_name:str|None=None
    description:str|None=None

class HeroResponseWithTeam(HeroResponse):
         team : TeamResponse 


     
POSTGRESS_DB = "postgresql://areebstudent567:g4bOtYWUfE9s@ep-fancy-glitter-82049478.us-east-2.aws.neon.tech/fastSqlModel?sslmode=require"
engine = create_engine(POSTGRESS_DB)


def create_table():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


def get_db():
    with Session(engine) as session:
        yield session
    


@app.on_event("startup") #lifecycle event-->function is supposed to be called when the application starts up, and it presumably calls the create_table()
def on_startup():
    create_table()


@app.get("/")
async def root():
    return {"message":"Hello World"}



#offset/limit
@app.get("/heroes" , response_model=list[Hero])
def get_heroes(session:Annotated[Session,Depends(get_db)],offset:int=Query(default= 0,le=4),limit:int=Query(default= 0,le=4)):
        heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
        return heroes





@app.get("/heroes/{hero_id}", response_model= HeroResponseWithTeam)
def get_hero(hero_id:int, session:Annotated[Session, Depends(get_db)]):
     hero = session.get(Hero, hero_id)
     if not hero:
          raise HTTPException(status_code=404, detail="Hero not found")
     print(hero.team)
     return hero


@app.post("/heroes",response_model=HeroResponse)
def create_hero(hero:HeroCreate,session:Annotated[Session,Depends(get_db)]):
        print("Data from client:",hero)
        #Data from client: name='Junaid' secret_name='JK' description='Hello'
        hero_insert = Hero.model_validate(hero)
        print("Data after validation:", hero_insert)
        #Data after validation: id=None name='Junaid' secret_name='JK' description='Hello'
        session.add(hero_insert)
        session.commit()
        session.refresh(hero_insert)
        return hero_insert



@app.patch("/heroes/{hero_id}", response_model=HeroResponse)
def update_hero(hero_id:int, hero_data:HeroUpdate, session:Annotated[Session, Depends(get_db)]):
    hero = session.get(Hero, hero_id)
    if not hero:
          raise HTTPException(status_code=404, detail="Hero not found")
    
    print("Hero in db:",hero)
    #Hero in db: secret_name='AA' id=1 description=None name='Ali Khan'
    print("Data from client:", hero_data)
    #Data from client: name='Areeb Ahmed' secret_name=None description=None
    hero_data_dict = hero_data.model_dump(exclude_unset=True) #model_dump dictionary mai convert kray ga or exclude_unset=True None attributes ko include nahi kray ga.
    print("Hero_dict_data:", hero_data_dict)
    #Hero_dict_data: {'name': 'Areeb Ahmed'}


    for key,value in hero_data_dict.items():
        setattr(hero, key, value)
    print("after:",hero)
    #after: secret_name='AA' id=1 description=None name='Areeb Ahmed'

    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id:int, session:Annotated[Session, Depends(get_db)]):
    hero = session.get(Hero, hero_id)
    if not hero:
          raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"message":"Hero deleted successfully"}


@app.get("/teams", response_model=list[Team])
def get_teams(session:Annotated[Session, Depends(get_db)]):
     
     teams = session.exec(select(Team)).all()
     return teams

@app.post("/teams", response_model=TeamResponse)
def create_team(team:TeamCreate, session:Annotated[Session, Depends(get_db)]):
    team_insert = Team.model_validate(team)
    session.add(team_insert)
    session.commit()
    session.refresh(team_insert)
    return team_insert


@app.get("/teams/{team_id}", response_model=TeamResponse)
def get_team(team_id:int, session:Annotated[Session, Depends(get_db)]):
     team = session.get(Team, team_id)
     if not team:
          raise HTTPException(status_code=404, detail="Team not found")
     return team


@app.patch("/teams/{team_id}", response_model=TeamResponse)
def update_team(team_id:int, team_data:TeamUpdate, session:Annotated[Session, Depends(get_db)]):
     team = session.get(Team, team_id)
     if not team:
          raise HTTPException(status_code=404, detail="Team not found")
     print("Team in db:", team)
     #Team in db: id=1 headquarter='Lahore' name='Team 1'
     print("Data from client:", team_data)
     #Data from client: name='Team 2' headquarter='Karachi'
     team_data_dict = team_data.model_dump(exclude_unset=True)
     print("Team_dict_data:", team_data_dict)
     #Team_dict_data: {'name': 'Team 2', 'headquarter': 'Karachi'}
     for key,value in team_data_dict.items():
          setattr(team, key, value)

     print("after:", team)
     #after: id=1 headquarter='Karachi' name='Team 2'

     session.add(team)
     session.commit()
     session.refresh(team)
     return team


@app.delete("/teams/{team_id}")
def delete_team(team_id:int, session:Annotated[Session, Depends(get_db)]):
     team = session.get(Team, team_id)
     if not team:
          raise HTTPException(status_code=404, detail="Team not found")
     session.delete(team)
     session.commit()
     return {"message":"Team deleted successfully"}

