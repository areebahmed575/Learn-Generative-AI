import warnings
import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel
from dotenv import load_dotenv, find_dotenv
from fastapi.middleware.cors import CORSMiddleware


warnings.filterwarnings("ignore")



load_dotenv(find_dotenv())


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"  
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")


from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InputDetails(SQLModel):
    location: str
    activity: str


class TaskOutput(SQLModel):
    task_description: str
    task_output: str


class CrewResult(SQLModel):
    combined_output: str
    tasks_output: Optional[List[TaskOutput]] = None 

@app.post("/process", response_model=CrewResult)
async def process_inputs(inputs_details: InputDetails):
    """
    Endpoint to process weather assessment and activity recommendation based on user inputs.
    
    Args:
        inputs_details (InputDetails): The input details containing location and activity.
    
    Returns:
        CrewResult: The combined output of all tasks and individual task outputs.
    """
    
    try:
       
        serper_tool = SerperDevTool()
        
       
        weather_analyst = Agent(
            role="Weather Analyst",
            goal="Provide weather assessments" 
            "for tourism {location}",
            backstory="An expert meteorologist"
            "specializing in tourism weather reports.",
            tools=[serper_tool],
            verbose=True,
            memory=False
        )
        
       
        activity_recommender = Agent(
            role="Activity Recommender",
            goal="Suggest {activity}" 
            "based on current weather conditions.",
            backstory=(
                "A tourism guide with in-depth knowledge "
                "of Pakistani tourist spots and weather safety."
            ),
            verbose=True,
            memory=False
        )
        
       
        weather_check_task = Task(
            description=(
                "Check the weather for the {location} "
                "and determine whether it's suitable "
                "for outdoor {activity}. "
                "Focus on temperature, "
                "and general conditions."
            ),
            expected_output="The weather will be fetched" 
            "dynamically by the agent.",
            agent=weather_analyst,
        )
        
       
        recommendation_task = Task(
            description=(
                "If the weather conditions are not ideal, "
                "recommend alternative {activity}. "
                "Consider factors like user preferences, "
                "location, and weather."
            ),
            expected_output="Recommend suitable tourist {activity}"
            "in {location} based on weather.",
            agent=activity_recommender,
        )
        
       
        crew = Crew(
            agents=[weather_analyst, activity_recommender],
            tasks=[weather_check_task, recommendation_task],
            process=Process.sequential,
            verbose=True 
        )
        
        
        input_data = {
            'location': inputs_details.location,
            'activity': inputs_details.activity
        }
        
        
        result = crew.kickoff(inputs=input_data)
        
        
        print(f"Type of result: {type(result)}")
        print(f"Result content: {result}")
        
        
        crew_result = CrewResult(combined_output=result)
        
        
        
        return crew_result
    
    except AttributeError as ae:
        
        raise HTTPException(status_code=500, detail=f"AttributeError: {str(ae)}")
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
