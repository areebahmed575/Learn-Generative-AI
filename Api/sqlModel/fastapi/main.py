from fastapi import FastAPI,Depends,HTTPException,Query
from sqlmodel import Field, SQLModel, create_engine,Session,select
from typing import Annotated


class HeroBase(SQLModel):
    name:str
    secret_name:str
    

class Hero(HeroBase,table=True):
    id:int|None =Field(default=None,primary_key=True)
    description:str|None=None

class HeroCreate(HeroBase):
    description:str|None=None
   


class HeroResponse(HeroBase):
    id:int
    description:str|None=None


class HeroUpdate(SQLModel):
    name:str|None=None
    secret_name:str|None=None
    description:str|None=None

     

     
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





@app.get("/heroes/{hero_id}", response_model=HeroResponse)
def get_hero(hero_id:int, session:Annotated[Session, Depends(get_db)]):
     hero = session.get(Hero, hero_id)
     if not hero:
          raise HTTPException(status_code=404, detail="Hero not found")
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

