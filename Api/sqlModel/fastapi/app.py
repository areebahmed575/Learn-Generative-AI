from fastApi import FastAPI
from sqlmodel import SQLModel,Field,create_engine,Session

class Hero(SQLModel,table=True):
    id:int|None =Field(default=None,primary_key=True)
    name:str = Field(index=True)
    secret_name:str
    description:str|None=None


POSTGRESS_DB = "postgresql://postgres:postgres@localhost:5432/fastapi"
engine = create_engine(POSTGRESS_DB)


def create_table():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

@app.on_event("startup") #lifecycle event
def on_startup():
    create_table()


@app.get("/")
async def root():
    return {"message":"Hello World"}


@app.get("/heroes")
def get_heroes():
    with Session(engine) as session:
        heroes = session.exec(Hero).all()
        return heroes

@app.post("/heroes")
def create_hero(hero:Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero