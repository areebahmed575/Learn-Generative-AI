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
    program_id : int
    instructot_id : int
    course_name: str
   


# class Students(SQLModel):
#     id: int | None = Field(default=None, primary_key=True)
#     student_name: str
#     student_email: str
#     student_password: str
#     course_id: int | None = Field(default=None, foreign_key="course.id")



class Topic(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    course_id: int | None = Field(default=None, foreign_key="course.id")
    topic_name: str
    topic_description: str

class Content(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    topic_id : int = Field(default=None, foreign_key="topic.id")

class Quiz(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    course_id: int | None = Field(default=None, foreign_key="course.id")
    quiz_name: str
    quiz_time: str
    quiz_description : str


class QuizTopics(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    topic_id: int | None = Field(default=None, foreign_key="topic.id")
    #parent_quiz_topic_id : Field(default=None, foreign_key="topic.id")
    quiz_name : str|None = None


class QuestionType(str, Enum):
    single_select = "single_select"
    multi_select = "multi_select"
    case_study = "case_study"
    free_text = "free_text"
    code_questions = "code_questions"
    


class Question(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    question_text: str
    question_type: QuestionType
    question_points: int


class SingleSelectMcqs(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    #mcqs_type :Enum


class MultiSelectMcqs(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    mcqs_id: int
    


class CaseStudy(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    mcqs_id : int

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
    correct_answer : str
    points_received : int 



class SingleSelectMcqsAns(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    answer_id: int | None = Field(default=None, foreign_key="answer.id")
    mcqs_id: int
    selected_mcqs_id: int


class MultiSelectMcqsAns(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    answer_id: int | None = Field(default=None, foreign_key="answer.id")
    mcqs_id: int
    

class OptionMultiSelectAnswer(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    multislelect_mcqs_id: int | None = Field(default=None, foreign_key="multiselect_mcqs.id")
    selected_mcqs_id: int

class CaseStudyAns(SQLModel):
    id : int | None = Field(default=None, primary_key=True)
    answer_id : int | None = Field(default=None, foreign_key="answer.id")

class JoinCaseStudyAnswer(SQLModel):
    id : int | None = Field(default=None, primary_key=True)
    case_study_id : int | None = Field(default=None, foreign_key="case_study.id")
    single_select_mcq_answer_id : int

class FreeTextAnswer(SQLModel):
    id : int | None = Field(default=None, primary_key=True)
    answer_id : int | None = Field(default=None, foreign_key="answer.id")
    field_answer : str

class CodingQuestionsAnswer(SQLModel):
    id : int | None = Field(default=None, primary_key=True)
    answer_id : int | None = Field(default=None, foreign_key="answer.id")
    field_answer : str
    

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
