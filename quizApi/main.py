from fastapi import FastAPI,Depends,HTTPException,Query
from sqlmodel import Field, SQLModel, create_engine,Session,select,Relationship
from typing import Annotated,Optional
from enum import Enum
from datetime import datetime
from fastapi import Depends



class Course(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    program_id : int
    instructor_id : int
    course_name: str
    topics : list["Topic"] = Relationship(back_populates="course")  # one to many
    quizes : list["Quiz"] = Relationship(back_populates="course")  # one to many or #one to one


class Topic(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    course_id: int | None = Field(default=None, foreign_key="course.id")
    topic_name: str
    topic_description: str
    course: Course = Relationship(back_populates="topics") # many to one
    contents: list["Content"] = Relationship(back_populates="topic") # one to many
    quiz_topics: list["QuizTopics"] = Relationship(back_populates="topic") # one to many

class Content(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    topic_id : Optional[int] = Field(foreign_key="topic.id")
    topic: Topic = Relationship(back_populates="contents") # many to one

class Quiz(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    course_id: int | None = Field(default=None, foreign_key="course.id")
    quiz_name: str
    quiz_time: datetime
    quiz_description : str
    course: Course = Relationship(back_populates="quizes") # many to one
    answer_sheets: list["AnswerSheet"] = Relationship(back_populates="quiz") # one to many
    quiz_topics: list["QuizTopics"] = Relationship(back_populates="quiz") # one to many


class QuizTopics(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    topic_id: int | None = Field(default=None, foreign_key="topic.id")
    parent_quiz_topic_id: int | None = Field(default=None, foreign_key="quiztopics.id")
    quiz_name : str|None = None
    quiz: Quiz = Relationship(back_populates="quiz_topics") # many to one
    topic: Topic = Relationship(back_populates="quiz_topics") # many to one

class QuestionType(str, Enum):
    single_select = "single_select"
    multi_select = "multi_select"
    case_study = "case_study"
    free_text = "free_text"
    code_questions = "code_questions"
    



class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    question_text: str
    question_type: QuestionType
    question_points: int
    single_select_mcqs: "SingleSelectMcqs" = Relationship(back_populates="question")
    multi_select_mcqs: "MultiSelectMcqs" = Relationship(back_populates="question")
    coding_questions: "CodingQuestions" = Relationship(back_populates="question")
    
    
class McqsType(str,Enum):
    type1: str = "Type 1"
    type2: str = "Type 2"
    type3: str = "Type 3"
    type4: str = "Type 4"    


  
class SingleSelectMcqs(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    mcqs_type: McqsType
    question: Question = Relationship(back_populates="single_select_mcqs") # one to one
    options: list["SingleOptions"] = Relationship(back_populates="single_select_mcqs") # one to many
    case_studies: list["CaseStudy"] = Relationship(back_populates="single_select_mcqs")




class SingleOptions(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    single_select_id : int | None = Field(default=None, foreign_key="singleselectmcqs.id")
    option_text : str
    is_correct : bool
    single_select_mcqs: SingleSelectMcqs = Relationship(back_populates="options") # many to one
    

class MultiSelectMcqs(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    mcqs_id: int
    question: Question = Relationship(back_populates="multi_select_mcqs") # one to one
    options: list["OptionMultiSelectQuestions"] = Relationship(back_populates="multi_select_mcqs") # one to many


    
class OptionMultiSelectQuestions(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    multi_select_id : int | None = Field(default=None, foreign_key="multiselectmcqs.id")
    option_text : str
    is_correct : bool
    multi_select_mcqs: MultiSelectMcqs = Relationship(back_populates="options") # many to one



class CaseStudy(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    single_select_mcqs_id: int | None = Field(default=None, foreign_key="singleselectmcqs.id")
    mcqs_id : int
    single_select_mcqs: SingleSelectMcqs = Relationship(back_populates="case_studies")  

class CodingQuestions(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    question_id: int | None = Field(default=None, foreign_key="question.id")
    is_correct: bool
    question: Question = Relationship(back_populates="coding_questions") # one to one




class AnswerSheet(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    quiz_id: int | None = Field(default=None, foreign_key="quiz.id")
    quiz_status: str
    start_date: datetime  
    end_date: datetime   
    answers: list["Answer"] = Relationship(back_populates="answer_sheet") # one to many
    quiz: Quiz = Relationship(back_populates="answer_sheets")  # Define the relationship with Quiz

class Answer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    correct_answer: str
    points_received: int
    answer_sheet_id: Optional[int] = Field(default=None, foreign_key="answersheet.id")
    answer_sheet: AnswerSheet = Relationship(back_populates="answers")  # many to one
    single_select_mcqs_ans: list["SingleSelectMcqsAns"] = Relationship(back_populates="answer")  # one to many
    multi_select_mcqs_ans: list["MultiSelectMcqsAns"] = Relationship(back_populates="answer")  # one to many
    case_study_ans: list["CaseStudyAns"] = Relationship(back_populates="answer")  # one to many
    coding_questions_answer: list["CodingQuestionsAnswer"] = Relationship(back_populates="answer")  # one to many


class SingleSelectMcqsAns(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    answer_id: int | None = Field(default=None, foreign_key="answer.id")
    mcqs_id: int
    selected_mcqs_id: int
    answer: Answer = Relationship(back_populates="single_select_mcqs_ans") # many to one


    


class MultiSelectMcqsAns(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    answer_id: int | None = Field(default=None, foreign_key="answer.id")
    mcqs_id: int
    answer: Answer = Relationship(back_populates="multi_select_mcqs_ans") # many to one
    options: list["OptionMultiSelectAnswer"] = Relationship(back_populates="multi_select_mcqs_ans") # one to many

class OptionMultiSelectAnswer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    multiselect_mcqs_ans_id: int | None = Field(default=None, foreign_key="multiselectmcqsans.id")
    selected_mcqs_id: int
    multi_select_mcqs_ans: MultiSelectMcqsAns = Relationship(back_populates="options") # many to one

class CaseStudyAns(SQLModel,table=True):
    id : int | None = Field(default=None, primary_key=True)
    answer_id : int | None = Field(default=None, foreign_key="answer.id")
    answer: Answer = Relationship(back_populates="case_study_ans") # many to one
    join_case_study_answer: list["JoinCaseStudyAnswer"] = Relationship(back_populates="case_study_ans") # one to many


class JoinCaseStudyAnswer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    case_study_ans_id: int | None = Field(default=None, foreign_key="casestudyans.id")
    single_select_mcq_answer_id: int
    case_study_ans: CaseStudyAns = Relationship(back_populates="join_case_study_answer")


class CodingQuestionsAnswer(SQLModel,table=True):
    id : int | None = Field(default=None, primary_key=True)
    answer_id : int | None = Field(default=None, foreign_key="answer.id")
    field_answer : str
    answer: Answer = Relationship(back_populates="coding_questions_answer") # many to one
   
    





POSTGRESS_DB = "postgresql://areebstudent567:g4bOtYWUfE9s@ep-fancy-glitter-82049478.us-east-2.aws.neon.tech/QuizApi?sslmode=require"
engine = create_engine(POSTGRESS_DB)   


def create_table():
    #SQLModel.metadata.drop_all(engine)
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



@app.get("/courses" , response_model = list[Course])
def get_courses(session: Annotated[Session, Depends(get_db)]):
    courses = session.exec(select(Course)).all()
    return courses


@app.post("/courses", response_model=Course)
def create_course(course: Course, session: Annotated[Session, Depends(get_db)]):
    print("Data from client:",course)
    course_insert = Course.model_validate(course)
    print("Data after validation:", course_insert)
    session.add(course_insert)
    session.commit()
    return course_insert



@app.get("/courses/{courses_id}", response_model= Course)
def get_hero(courses_id:int, session:Annotated[Session, Depends(get_db)]):
     course = session.get(Course, courses_id)
     if not course:
          raise HTTPException(status_code=404, detail="Course not found")
     print(course.course_name)
     return course

@app.get("/topics", response_model=list[Topic])
def get_topics(session: Session = Depends(get_db)):
    topics = session.exec(select(Topic)).all()
    return topics

@app.post("/topics", response_model=Topic)
def create_topic(topic: Topic, session: Session = Depends(get_db)):
    existing_course = session.exec(select(Course).filter(Course.id == topic.course_id)).first()
    if not existing_course:
        raise HTTPException(status_code=400, detail="The specified course does not exist.")

    topic.course = existing_course
    session.add(topic)
    session.commit()
    session.refresh(topic)

    return topic


@app.get("/topics/{topic_id}", response_model=Topic)
def get_topic(topic_id: int, session: Session = Depends(get_db)):
    topic = session.get(Topic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic
    
@app.get("/quizzes", response_model=list[Quiz])
def get_quizzes(session: Session = Depends(get_db)):
    quizzes = session.exec(select(Quiz)).all()
    return quizzes

# @app.post("/quizzes", response_model=Quiz)
# def create_quiz(quiz: Quiz, session: Session = Depends(get_db)):
#     existing_quiz = session.exec(select(Course).filter(Course.id == quiz.course_id)).first()
#     if not existing_quiz:
#         raise HTTPException(status_code=400, detail="The specified course does not exist.")

#     quiz.course = existing_quiz
#     session.add(quiz)
#     session.commit()
#     session.refresh(quiz)

#     return quiz
    
@app.post("/quizzes", response_model=Quiz)
def create_quiz(quiz: Quiz, session: Session = Depends(get_db)):
    existing_course = session.get(Course, quiz.course_id)
    if not existing_course:
        raise HTTPException(status_code=400, detail="The specified course does not exist.")

    # Since we found the existing course, we assign it to the quiz
    quiz.course = existing_course

    session.add(quiz)
    session.commit()
    session.refresh(quiz)

    return quiz





@app.get("/quizzes/{quiz_id}", response_model=Quiz)
def get_quiz(quiz_id: int, session: Session = Depends(get_db)):
    quiz = session.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz







@app.get("/quiztopics", response_model=list[QuizTopics])
def get_quiz_topics(session: Session = Depends(get_db)):
    quiz_topics = session.exec(select(QuizTopics)).all()
    return quiz_topics

@app.post("/quiztopics", response_model=QuizTopics)
def create_quiz_topic(quiz_topic: QuizTopics, session: Session = Depends(get_db)):
    # Validate if the quiz_id and topic_id are valid
    existing_quiz = session.get(Quiz, quiz_topic.quiz_id)
    existing_topic = session.get(Topic, quiz_topic.topic_id)
    if not existing_quiz or not existing_topic:
        raise HTTPException(status_code=400, detail="Invalid quiz_id or topic_id")

    # Create a new QuizTopics object
    new_quiz_topic = QuizTopics(
        quiz_id=quiz_topic.quiz_id,
        topic_id=quiz_topic.topic_id,
        parent_quiz_topic_id=quiz_topic.parent_quiz_topic_id,
        quiz_name=quiz_topic.quiz_name
    )

    # Add the new_quiz_topic to the session and commit the transaction
    session.add(new_quiz_topic)
    session.commit()
    session.refresh(new_quiz_topic)

    return new_quiz_topic



@app.get("/quiztopics/{quiz_topic_id}", response_model=QuizTopics)
def get_quiz_topic(quiz_topic_id: int, session: Session = Depends(get_db)):
    quiz_topic = session.get(QuizTopics, quiz_topic_id)
    if not quiz_topic:
        raise HTTPException(status_code=404, detail="Quiz Topic not found")
    return quiz_topic    

@app.get("/contents", response_model=list[Content])
def get_contents(session: Session = Depends(get_db)):
    contents = session.exec(select(Content)).all()
    return contents


@app.post("/contents", response_model=Content)
def create_content(content: Content, session: Session = Depends(get_db)):
    # Ensure that the provided topic_id exists
    if content.topic_id is None:
        raise HTTPException(status_code=400, detail="topic_id is required for Content creation")

    topic = session.get(Topic, content.topic_id)
    if topic is None:
        raise HTTPException(status_code=400, detail="Invalid topic_id provided")

    
    content_insert = Content(**content.model_dump())

    session.add(content_insert)
    session.commit()
    session.refresh(content_insert)
    return content_insert



@app.get("/contents/{content_id}", response_model=Content)
def get_content(content_id: int, session: Session = Depends(get_db)):
    content = session.get(Content, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content



@app.get("/questions", response_model=list[Question])
def get_questions(session: Session = Depends(get_db)):
    questions = session.exec(select(Question)).all()
    return questions

@app.post("/questions", response_model=Question)
def create_question(question: Question, session: Session = Depends(get_db)):
    print("Data from client:",question)
    question_insert = Question.model_validate(question)
    session.add(question_insert)
    session.commit()
    session.refresh(question_insert)
    return question_insert

@app.get("/questions/{question_id}", response_model=Question)
def get_question(question_id: int, session: Session = Depends(get_db)):
    question = session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@app.get("/singleselectmcqs", response_model=list[SingleSelectMcqs])
def get_single_select_mcqs(session: Session = Depends(get_db)):
    single_select_mcqs = session.exec(select(SingleSelectMcqs)).all()
    return single_select_mcqs

@app.post("/singleselectmcqs", response_model=SingleSelectMcqs)
def create_single_select_mcqs(single_select_mcqs: SingleSelectMcqs, session: Session = Depends(get_db)):
    # Validate if the question_id and case_study_id are valid
    existing_question = session.get(Question, single_select_mcqs.question_id)
    if not existing_question :
        raise HTTPException(status_code=400, detail="Invalid question_id or case_study_id")

    # Create a new SingleSelectMcqs object
    new_single_select_mcqs = SingleSelectMcqs(
        question_id=single_select_mcqs.question_id,
        mcqs_type=single_select_mcqs.mcqs_type,
    )

    # Add the new_single_select_mcqs to the session and commit the transaction
    session.add(new_single_select_mcqs)
    session.commit()
    session.refresh(new_single_select_mcqs)

    return new_single_select_mcqs

@app.get("/singleselectmcqs/{singleselectmcqs_id}", response_model=SingleSelectMcqs)
def get_single_select_mcq(singleselectmcqs_id: int, session: Session = Depends(get_db)):
    single_select_mcqs = session.get(SingleSelectMcqs, singleselectmcqs_id)
    if not single_select_mcqs:
        raise HTTPException(status_code=404, detail="Single Select MCQ not found")
    return single_select_mcqs

@app.get("/singleoptions", response_model=list[SingleOptions])
def get_single_options(session: Session = Depends(get_db)):
    single_options = session.exec(select(SingleOptions)).all()
    return single_options

@app.post("/singleoptions", response_model=SingleOptions)
def create_single_option(single_option: SingleOptions, session: Session = Depends(get_db)):
    # Validate if the single_select_id is valid
    existing_single_select_mcqs = session.get(SingleSelectMcqs, single_option.single_select_id)
    if not existing_single_select_mcqs:
        raise HTTPException(status_code=400, detail="Invalid single_select_id")

    # Create a new SingleOptions object
    new_single_option = SingleOptions(
        single_select_id=single_option.single_select_id,
        option_text=single_option.option_text,
        is_correct=single_option.is_correct
    )

    # Add the new_single_option to the session and commit the transaction
    session.add(new_single_option)
    session.commit()
    session.refresh(new_single_option)

    return new_single_option



@app.get("/singleoptions/{singleoptions_id}", response_model=SingleOptions)
def get_single_option(singleoptions_id: int, session: Session = Depends(get_db)):
    single_option = session.get(SingleOptions, singleoptions_id)
    if not single_option:
        raise HTTPException(status_code=404, detail="Single Option not found")
    return single_option

@app.get("/multiselectmcqs", response_model=list[MultiSelectMcqs])
def get_multi_select_mcqs(session: Session = Depends(get_db)):
    multi_select_mcqs = session.exec(select(MultiSelectMcqs)).all()
    return multi_select_mcqs

@app.post("/multiselectmcqs", response_model=MultiSelectMcqs)
def create_multi_select_mcqs(multi_select_mcqs: MultiSelectMcqs, session: Session = Depends(get_db)):
    # Assuming 'question_id' is properly provided in the MultiSelectMcqs instance
    # Validate the incoming MultiSelectMcqs object
    if not multi_select_mcqs.question_id:
        raise HTTPException(status_code=400, detail="Missing question_id")

    # Add the MultiSelectMcqs instance to the session and commit the transaction
    session.add(multi_select_mcqs)
    session.commit()
    session.refresh(multi_select_mcqs)

    return multi_select_mcqs


@app.get("/multiselectmcqs/{multiselectmcqs_id}", response_model=MultiSelectMcqs)
def get_multi_select_mcq(multiselectmcqs_id: int, session: Session = Depends(get_db)):
    multi_select_mcqs = session.get(MultiSelectMcqs, multiselectmcqs_id)
    if not multi_select_mcqs:
        raise HTTPException(status_code=404, detail="Multi Select MCQ not found")
    return multi_select_mcqs

@app.get("/optionmultiselectquestions", response_model=list[OptionMultiSelectQuestions])
def get_option_multi_select_questions(session: Session = Depends(get_db)):
    option_multi_select_questions = session.exec(select(OptionMultiSelectQuestions)).all()
    return option_multi_select_questions

@app.post("/optionmultiselectquestions", response_model=OptionMultiSelectQuestions)
def create_option_multi_select_question(option_multi_select_question: OptionMultiSelectQuestions, session: Session = Depends(get_db)):
    # Assuming 'multi_select_id' is properly provided in the OptionMultiSelectQuestions instance
    # Validate the incoming OptionMultiSelectQuestions object
    if not option_multi_select_question.multi_select_id:
        raise HTTPException(status_code=400, detail="Missing multi_select_id")

    # Add the OptionMultiSelectQuestions instance to the session and commit the transaction
    session.add(option_multi_select_question)
    session.commit()
    session.refresh(option_multi_select_question)

    return option_multi_select_question


@app.get("/optionmultiselectquestions/{optionmultiselectquestions_id}", response_model=OptionMultiSelectQuestions)
def get_option_multi_select_question(optionmultiselectquestions_id: int, session: Session = Depends(get_db)):
    option_multi_select_question = session.get(OptionMultiSelectQuestions, optionmultiselectquestions_id)
    if not option_multi_select_question:
        raise HTTPException(status_code=404, detail="Option Multi Select Question not found")
    return option_multi_select_question

@app.get("/casestudies", response_model=list[CaseStudy])
def get_case_studies(session: Session = Depends(get_db)):
    case_studies = session.exec(select(CaseStudy)).all()
    return case_studies

@app.post("/casestudies", response_model=CaseStudy)
def create_case_study(case_study: CaseStudy, session: Session = Depends(get_db)):
    # Assuming 'single_select_mcqs_id' is properly provided in the CaseStudy instance
    # Validate the incoming CaseStudy object
    if not case_study.single_select_mcqs_id:
        raise HTTPException(status_code=400, detail="Missing single_select_mcqs_id")

    # Add the CaseStudy instance to the session and commit the transaction
    session.add(case_study)
    session.commit()
    session.refresh(case_study)

    return case_study


@app.get("/casestudies/{casestudies_id}", response_model=CaseStudy)
def get_case_study(casestudies_id: int, session: Session = Depends(get_db)):
    case_study = session.get(CaseStudy, casestudies_id)
    if not case_study:
        raise HTTPException(status_code=404, detail="Case Study not found")
    return case_study

@app.get("/codingquestions", response_model=list[CodingQuestions])
def get_coding_questions(session: Session = Depends(get_db)):
    coding_questions = session.exec(select(CodingQuestions)).all()
    return coding_questions

@app.post("/codingquestions", response_model=CodingQuestions)
def create_coding_question(coding_question: CodingQuestions, session: Session = Depends(get_db)):
    # Assuming 'question_id' is properly provided in the CodingQuestions instance
    # Validate the incoming CodingQuestions object
    if not coding_question.question_id:
        raise HTTPException(status_code=400, detail="Missing question_id")

    # Add the CodingQuestions instance to the session and commit the transaction
    session.add(coding_question)
    session.commit()
    session.refresh(coding_question)

    return coding_question


@app.get("/codingquestions/{codingquestions_id}", response_model=CodingQuestions)
def get_coding_question(codingquestions_id: int, session: Session = Depends(get_db)):
    coding_question = session.get(CodingQuestions, codingquestions_id)
    if not coding_question:
        raise HTTPException(status_code=404, detail="Coding Question not found")
    return coding_question




@app.get("/answersheets", response_model=list[AnswerSheet])
def get_answer_sheets(session: Session = Depends(get_db)):
    answer_sheets = session.exec(select(AnswerSheet)).all()
    return answer_sheets

@app.post("/answersheets", response_model=AnswerSheet)
def create_answer_sheet(answer_sheet: AnswerSheet, session: Session = Depends(get_db)):
    # Assuming 'quiz_id' is properly provided in the AnswerSheet instance
    # Validate the incoming AnswerSheet object
    if not answer_sheet.quiz_id:
        raise HTTPException(status_code=400, detail="Missing quiz_id")

    # Add the AnswerSheet instance to the session and commit the transaction
    session.add(answer_sheet)
    session.commit()
    session.refresh(answer_sheet)

    return answer_sheet

@app.get("/answersheets/{answer_sheet_id}", response_model=AnswerSheet)
def get_answer_sheet(answer_sheet_id: int, session: Session = Depends(get_db)):
    answer_sheet = session.get(AnswerSheet, answer_sheet_id)
    if not answer_sheet:
        raise HTTPException(status_code=404, detail="Answer Sheet not found")
    return answer_sheet

@app.get("/answers", response_model=list[Answer])
def get_answers(session: Session = Depends(get_db)):
    answers = session.exec(select(Answer)).all()
    return answers

@app.post("/answers", response_model=Answer)
def create_answer(answer: Answer, session: Session = Depends(get_db)):
    # Assuming 'answer_sheet_id' is properly provided in the Answer instance
    # Validate the incoming Answer object
    if not answer.answer_sheet_id:
        raise HTTPException(status_code=400, detail="Missing answer_sheet_id")

    # Add the Answer instance to the session and commit the transaction
    session.add(answer)
    session.commit()
    session.refresh(answer)

    return answer


@app.get("/answers/{answer_id}", response_model=Answer)
def get_answer(answer_id: int, session: Session = Depends(get_db)):
    answer = session.get(Answer, answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer


@app.get("/singleselectmcqsans", response_model=list[SingleSelectMcqsAns])
def get_single_select_mcqs_ans(session: Session = Depends(get_db)):
    single_select_mcqs_ans = session.exec(select(SingleSelectMcqsAns)).all()
    return single_select_mcqs_ans


@app.post("/singleselectmcqsans", response_model=SingleSelectMcqsAns)
def create_single_select_mcqs_ans(single_select_mcqs_ans: SingleSelectMcqsAns, session: Session = Depends(get_db)):
    # Assuming 'answer_id' is properly provided in the SingleSelectMcqsAns instance
    # Validate the incoming SingleSelectMcqsAns object
    if not single_select_mcqs_ans.answer_id:
        raise HTTPException(status_code=400, detail="Missing answer_id")

    # Add the SingleSelectMcqsAns instance to the session and commit the transaction
    session.add(single_select_mcqs_ans)
    session.commit()
    session.refresh(single_select_mcqs_ans)

    return single_select_mcqs_ans

@app.get("/singleselectmcqsans/{singleselectmcqsans_id}", response_model=SingleSelectMcqsAns)
def get_single_select_mcqs_ans(singleselectmcqsans_id: int, session: Session = Depends(get_db)):
    single_select_mcqs_ans = session.get(SingleSelectMcqsAns, singleselectmcqsans_id)
    if not single_select_mcqs_ans:
        raise HTTPException(status_code=404, detail="Single Select MCQs Answer not found")
    return single_select_mcqs_ans

@app.get("/multiselectmcqsans", response_model=list[MultiSelectMcqsAns])
def get_multi_select_mcqs_ans(session: Session = Depends(get_db)):
    multi_select_mcqs_ans = session.exec(select(MultiSelectMcqsAns)).all()
    return multi_select_mcqs_ans

@app.post("/multiselectmcqsans", response_model=MultiSelectMcqsAns)
def create_multi_select_mcqs_ans(multi_select_mcqs_ans: MultiSelectMcqsAns, session: Session = Depends(get_db)):
    # Assuming 'answer_id' is properly provided in the MultiSelectMcqsAns instance
    # Validate the incoming MultiSelectMcqsAns object
    if not multi_select_mcqs_ans.answer_id:
        raise HTTPException(status_code=400, detail="Missing answer_id")

    # Add the MultiSelectMcqsAns instance to the session and commit the transaction
    session.add(multi_select_mcqs_ans)
    session.commit()
    session.refresh(multi_select_mcqs_ans)

    return multi_select_mcqs_ans


@app.get("/multiselectmcqsans/{multiselectmcqsans_id}", response_model=MultiSelectMcqsAns)
def get_multi_select_mcqs_ans(multiselectmcqsans_id: int, session: Session = Depends(get_db)):
    multi_select_mcqs_ans = session.get(MultiSelectMcqsAns, multiselectmcqsans_id)
    if not multi_select_mcqs_ans:
        raise HTTPException(status_code=404, detail="Multi Select MCQs Answer not found")
    return multi_select_mcqs_ans


@app.get("/optionmultiselectanswers", response_model=list[OptionMultiSelectAnswer])
def get_option_multi_select_answers(session: Session = Depends(get_db)):
    option_multi_select_answers = session.exec(select(OptionMultiSelectAnswer)).all()
    return option_multi_select_answers

@app.post("/optionmultiselectanswers", response_model=OptionMultiSelectAnswer)
def create_option_multi_select_answer(option_multi_select_answer: OptionMultiSelectAnswer, session: Session = Depends(get_db)):
    # Assuming 'multiselect_mcqs_ans_id' is properly provided in the OptionMultiSelectAnswer instance
    # Validate the incoming OptionMultiSelectAnswer object
    if not option_multi_select_answer.multiselect_mcqs_ans_id:
        raise HTTPException(status_code=400, detail="Missing multiselect_mcqs_ans_id")

    # Add the OptionMultiSelectAnswer instance to the session and commit the transaction
    session.add(option_multi_select_answer)
    session.commit()
    session.refresh(option_multi_select_answer)

    return option_multi_select_answer

@app.get("/optionmultiselectanswers/{optionmultiselectanswers_id}", response_model=OptionMultiSelectAnswer)
def get_option_multi_select_answer(optionmultiselectanswers_id: int, session: Session = Depends(get_db)):
    option_multi_select_answer = session.get(OptionMultiSelectAnswer, optionmultiselectanswers_id)
    if not option_multi_select_answer:
        raise HTTPException(status_code=404, detail="Option Multi Select Answer not found")
    return option_multi_select_answer


@app.get("/casestudyans", response_model=list[CaseStudyAns])
def get_case_study_answers(session: Session = Depends(get_db)):
    case_study_answers = session.exec(select(CaseStudyAns)).all()
    return case_study_answers

@app.post("/casestudyans", response_model=CaseStudyAns)
def create_case_study_answer(case_study_answer: CaseStudyAns, session: Session = Depends(get_db)):
    # Assuming 'answer_id' is properly provided in the CaseStudyAns instance
    # Validate the incoming CaseStudyAns object
    if not case_study_answer.answer_id:
        raise HTTPException(status_code=400, detail="Missing answer_id")

    # Add the CaseStudyAns instance to the session and commit the transaction
    session.add(case_study_answer)
    session.commit()
    session.refresh(case_study_answer)

    return case_study_answer


@app.get("/casestudyans/{casestudyans_id}", response_model=CaseStudyAns)
def get_case_study_answer(casestudyans_id: int, session: Session = Depends(get_db)):
    case_study_answer = session.get(CaseStudyAns, casestudyans_id)
    if not case_study_answer:
        raise HTTPException(status_code=404, detail="Case Study Answer not found")
    return case_study_answer

@app.get("/joincasestudyanswers", response_model=list[JoinCaseStudyAnswer])
def get_join_case_study_answers(session: Session = Depends(get_db)):
    join_case_study_answers = session.exec(select(JoinCaseStudyAnswer)).all()
    return join_case_study_answers

@app.post("/joincasestudyanswers", response_model=JoinCaseStudyAnswer)
def create_join_case_study_answer(join_case_study_answer: JoinCaseStudyAnswer, session: Session = Depends(get_db)):
    # Assuming 'case_study_ans_id' is properly provided in the JoinCaseStudyAnswer instance
    # Validate the incoming JoinCaseStudyAnswer object
    if not join_case_study_answer.case_study_ans_id:
        raise HTTPException(status_code=400, detail="Missing case_study_ans_id")

    # Add the JoinCaseStudyAnswer instance to the session and commit the transaction
    session.add(join_case_study_answer)
    session.commit()
    session.refresh(join_case_study_answer)

    return join_case_study_answer


@app.get("/joincasestudyanswers/{joincasestudyanswers_id}", response_model=JoinCaseStudyAnswer)
def get_join_case_study_answer(joincasestudyanswers_id: int, session: Session = Depends(get_db)):
    join_case_study_answer = session.get(JoinCaseStudyAnswer, joincasestudyanswers_id)
    if not join_case_study_answer:
        raise HTTPException(status_code=404, detail="Join Case Study Answer not found")
    return join_case_study_answer

@app.get("/codingquestionsanswers", response_model=list[CodingQuestionsAnswer])
def get_coding_questions_answers(session: Session = Depends(get_db)):
    coding_questions_answers = session.exec(select(CodingQuestionsAnswer)).all()
    return coding_questions_answers

@app.post("/codingquestionsanswers", response_model=CodingQuestionsAnswer)
def create_coding_questions_answer(coding_questions_answer: CodingQuestionsAnswer, session: Session = Depends(get_db)):
    # Assuming 'answer_id' is properly provided in the CodingQuestionsAnswer instance
    # Validate the incoming CodingQuestionsAnswer object
    if not coding_questions_answer.answer_id:
        raise HTTPException(status_code=400, detail="Missing answer_id")

    # Add the CodingQuestionsAnswer instance to the session and commit the transaction
    session.add(coding_questions_answer)
    session.commit()
    session.refresh(coding_questions_answer)

    return coding_questions_answer


@app.get("/codingquestionsanswers/{codingquestionsanswers_id}", response_model=CodingQuestionsAnswer)
def get_coding_questions_answer(codingquestionsanswers_id: int, session: Session = Depends(get_db)):
    coding_questions_answer = session.get(CodingQuestionsAnswer, codingquestionsanswers_id)
    if not coding_questions_answer:
        raise HTTPException(status_code=404, detail="Coding Questions Answer not found")
    return coding_questions_answer
