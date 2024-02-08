from sqlmodel import Field, SQLModel,Relationship

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



    

class HeroBase(SQLModel):
    name:str = Field(index=True)
    secret_name:str
    

class Hero(HeroBase,table=True):
    id:int|None =Field(default=None,primary_key=True)
    description:str|None=None
    team_id:int|None=Field(default=None, foreign_key="team.id")
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
