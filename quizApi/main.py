from fastapi import FastAPI,Depends,HTTPException,Query
from sqlmodel import Field, SQLModel, create_engine,Session,select
from typing import Annotated


class Admin(table=True):
   id:int|None = Field(default=None,primary_key=True)
   username : str
   email : str
   password : str

class User(table=True):
   id:int|None = Field(default=None, primary_key=True)
   username : str
   email : str
   password : str


class UserCreate(SQLModel):
   username : str
   email : str
   password : str
   
class UserRead(SQLModel):
   username : str
   email : str
   password : str
   id:int|None = Field(default=None, primary_key=True)

class UserUpdate(SQLModel):
   username : str|None=None
   email : str|None=None
   password : str|None=None
   id:int|None = Field(default=None, primary_key=True)

class UserResponse(SQLModel):
   username : str
   email : str
   password : str
   id:int|None = Field(default=None, primary_key=True)

class UserResponseWithAdmin(UserResponse):
   admin:Admin = Relationship(back_populates="users")

class AdminCreate(SQLModel):
   username : str
   email : str
   password : str
   users:list[UserCreate] = []

class AdminRead(SQLModel):
   username : str
   email : str
   password : str
   id:int|None = Field(default=None, primary_key=True)
   users:list[UserRead] = []

class AdminUpdate(SQLModel):
   username : str|None=None
   email : str|None=None
   password : str|None=None
   id:int|None = Field(default=None, primary_key=True)
   users:list[UserUpdate] = []
   users:list[UserCreate] = []

class AdminResponse(SQLModel):
   username : str
   email : str
   password : str
   id:int|None = Field(default=None, primary_key=True)
   users:list[UserResponse] = []
   users:list[UserCreate] = []


class Topic(SQLModel):
   id:int|None = Field(default=None, primary_key=True)
   course_id:int #Fk
   topic:str
   description:str

class QuizTopics(SQLModel):
   id:int|None = Field(default=None, primary_key=True)
   quiz_id:int #Fk
   topic_id:int #Fk

class Quiz(SQLModel):
   id:int|None = Field(default=None, primary_key=True)
   course_id:int #Fk
   quiz_name:str
   quiz_time:str
   quiz_list:list[QuizTopics] = []

class Question(SQLModel):
   id:int|None = Field(default=None, primary_key=True)
   quiz_id:int #Fk
   question_text:str
   question_type:str #check
   question_points:int
   

class MultiSelect():
   id:int|None = Field(default=None, primary_key=True)
   question_id:int #Fk
   option_text:str
   is_correct:bool
   option_id:int #Fk    


class SingleMcqs(SQLModel):
   id:int|None = Field(default=None, primary_key=True)
   question_id:int #Fk
   option_text:str
   is_correct:bool
   option_id:int #Fk

class CaseStudies(SQLModel):
   id:int|None = Field(default=None, primary_key=True)
   question_id:int #Fk
   option_text:str
   is_correct:bool
   option_id:int #Fk

class CodingQuestions(SQLModel):
   id:int|None = Field(default=None, primary_key=True)
   question_id:int #Fk
   option_text:str
   is_correct:bool
   option_id:int #Fk   

#class FreeTextQuestions(SQLModel):

class AnswerSheets(SQLModel):
   id:int|None = Field(default=None, primary_key=True)
   user_id:int #Fk
   quiz_status : str #check
   start_date : str
   end_date : str

class Answer(SQLModel):
   id:int|None = Field(default=None, primary_key=True)
   answer_sheet_id:int #Fk
   question_id:int #Fk
   answer_text:str
   answer_type:str #check
   answer_points:int
   answer_id:int #Fk


app = FastAPI()




   
