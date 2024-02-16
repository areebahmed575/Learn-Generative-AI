from fastapi import FastAPI,Depends,HTTPException,Query
from sqlmodel import Field, SQLModel, create_engine,Session,select
from typing import Annotated
from enum import Enum

# class Admin(table=True):
#    id:int|None = Field(default=None,primary_key=True)
#    username : str
#    email : str
#    password : str

# class User(table=True):
#    id:int|None = Field(default=None, primary_key=True)
#    username : str
#    email : str
#    password : str


# class UserCreate(SQLModel):
#    username : str
#    email : str
#    password : str
   
# class UserRead(SQLModel):
#    username : str
#    email : str
#    password : str
#    id:int|None = Field(default=None, primary_key=True)

# class UserUpdate(SQLModel):
#    username : str|None=None
#    email : str|None=None
#    password : str|None=None
#    id:int|None = Field(default=None, primary_key=True)

# class UserResponse(SQLModel):
#    username : str
#    email : str
#    password : str
#    id:int|None = Field(default=None, primary_key=True)

# class UserResponseWithAdmin(UserResponse):
#    admin:Admin = Relationship(back_populates="users")

# class AdminCreate(SQLModel):
#    username : str
#    email : str
#    password : str
#    users:list[UserCreate] = []

# class AdminRead(SQLModel):
#    username : str
#    email : str
#    password : str
#    id:int|None = Field(default=None, primary_key=True)
#    users:list[UserRead] = []

# class AdminUpdate(SQLModel):
#    username : str|None=None
#    email : str|None=None
#    password : str|None=None
#    id:int|None = Field(default=None, primary_key=True)
#    users:list[UserUpdate] = []
#    users:list[UserCreate] = []

# class AdminResponse(SQLModel):
#    username : str
#    email : str
#    password : str
#    id:int|None = Field(default=None, primary_key=True)
#    users:list[UserResponse] = []
#    users:list[UserCreate] = []

class Course(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    course_name: str
    course_description: str


class Topic(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    course_id: int | None = Field(default=None, foreign_key="course.id")
    topic_name: str
    description: str


class Quiz(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    course_id: int | None = Field(default=None, foreign_key="course.id")
    quiz_name: str
    quiz_time: str


class QuizTopics(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    topic_id: int | None = Field(default=None, foreign_key="topic.id")


class QuestionType(str, Enum):
    single_select = "single_select"
    multi_select = "multi_select"
    free_text = "free_text"
    code_questions = "code_questions"


class Question(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    topic_id: int | None = Field(default=None, foreign_key="topic.id")
    question_text: str
    question_type: QuestionType
    question_points: int


class MultiSelect(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    mcqs_id: int
    option_text: str
    is_correct: bool


class SingleSelect(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    mcqs_id: int
    option_text: str
    is_correct: bool


class CaseStudy(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    option_text: str
    is_correct: bool


class CodingQuestions(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    is_correct: bool


class AnswerSheet(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    quiz_status: str
    start_date: str  # Consider using datetime instead
    end_date: str  # Consider using datetime instead


class Answer(SQLModel):
    id: int | None = Field(default=None, primary_key=True)  


app = FastAPI()



POSTGRESS_DB = "postgresql://areebstudent567:g4bOtYWUfE9s@ep-fancy-glitter-82049478.us-east-2.aws.neon.tech/QuizApi?sslmode=require"
engine = create_engine(POSTGRESS_DB)   


def create_table():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


def get_db():
    with Session(engine) as session:
        yield session
    


@app.on_event("startup") 
def on_startup():
    create_table()


@app.get("/")
async def root():
    return {"message":"Hello World"}
