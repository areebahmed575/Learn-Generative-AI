#sql model is a wrapper top of pydantic and sqlalchemy
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine,Session,select


class Hero(SQLModel, table=True): #table=true for creating table
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


database_connection = "postgresql://areebstudent567:g4bOtYWUfE9s@ep-fancy-glitter-82049478.us-east-2.aws.neon.tech/sqlModel?sslmode=require"
engine = create_engine(database_connection,echo=True) #,echo=true means k jo query chal rahe h woh console mai dhekaye


# hero_1 = Hero(name="Areeb Ahmed", secret_name="AA")
# hero_2 = Hero(name="Ali Khan", secret_name="AK")
# hero_3 = Hero(name="Malaika Tanvir", secret_name="MT",age=22)

# with Session(engine) as session:
#     session.add(hero_1)
#     session.add(hero_2)
#     session.add(hero_3)
#     session.commit()


def create_hero():
    hero_1 = Hero(name="Areeb Ahmed", secret_name="AA")
    hero_2 = Hero(name="Ali Khan", secret_name="AK")
    hero_3 = Hero(name="Malaika Tanvir", secret_name="MT",age=22)

    session = Session(engine) 
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()
    session.close()
  

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_hero():
    session = Session(engine)
    statement = select(Hero)
    results = session.exec(statement)
    print(results.all())
       

def get_name():
    session = Session(engine)
    statement = select(Hero)
    results = session.exec(statement)
    #print(results.all())
    for heros in results:
        print(heros.name)    

def get_where_hero():
    session = Session(engine)
    statement = select(Hero).where(Hero.age == None)
    results = session.exec(statement)
    print(results.all())

def get_ind_hero():
    session = Session(engine)
    statement = select(Hero).where(Hero.name == "Areeb Ahmed")
    results = session.exec(statement)
    print(results.all())


def get_first_hero():
    session = Session(engine)
    statement = select(Hero).where(Hero.name == "Areeb Ahmed")
    results = session.exec(statement)
    print(results.first())

def get_one_hero():
    session = Session(engine)
    statement = select(Hero).where(Hero.id == 1) #id==1 srif 1 h otherwise error
    results = session.exec(statement)
    print(results.one())

def get_limit_hero():
    session = Session(engine)
    statement = select(Hero.name).limit(3) #shuru ki 3
    results = session.exec(statement)
    print(results.all())   


def get_offset_hero():
    session = Session(engine)
    statement = select(Hero.name).offset(2).limit(2) #shuru ki 2 chur kar agli 2
    results = session.exec(statement)
    print(results.all())

def update_first_age():
    session = Session(engine)
    statement = select(Hero).where(Hero.name == "Areeb Ahmed" and Hero.age == None)
    results = session.exec(statement)
    hero = results.first()
    hero.age = 22
    session.add(hero)
    session.commit()
    session.close()

def update_age():
    session = Session(engine)
    statement = select(Hero).where(Hero.name == "Areeb Ahmed")
    results = session.exec(statement)

    for row in results:
        hero = row[0]  # Assuming the Hero object is the first column in the result row
        hero.age = 23

    session.commit()
    session.close()

def delete_first_name():
    session = Session(engine)
    statement = select(Hero).where(Hero.name == "Areeb Ahmed")
    results = session.exec(statement).first()
    session.delete(results)
    session.commit()
    session.close()

def delete_all_name():
    session = Session(engine)
    statement = select(Hero).where(Hero.name == "Areeb Ahmed")
    results = session.exec(statement).all()
    for row in results:
        session.delete(row)
    session.commit()
    session.close()
    



print(__name__)
if __name__ == "__main__": #yeh file jab he chalay ghi jab name main hogha
    #create_db_and_tables()
     delete_all_name()
