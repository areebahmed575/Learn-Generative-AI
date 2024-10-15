import warnings
warnings.filterwarnings("ignore")

from fastapi import FastAPI
from sqlmodel import SQLModel
from typing import List
import os
import logging
from dotenv import load_dotenv, find_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
from fastapi.middleware.cors import CORSMiddleware

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv(find_dotenv())

# Set environment variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"  # or whichever model you're using
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input model
class InputDetails(SQLModel):
    search_query: str
    budget: str
    interest: str
    duration: str
    flight_search: str
    hotel_search: str
    restaurant_search: str

# Define output models
class TaskOutput(SQLModel):
    task_description: str
    task_output: str

class CrewResult(SQLModel):
    combined_output: str
    tasks_output: List[TaskOutput]
    individual_task_results: List[TaskOutput] = []

@app.post("/process", response_model=CrewResult)
async def process_inputs(inputs_details: InputDetails):
    logging.info(f"Received input: {inputs_details.dict()}")

    # Initialize tools
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    flight_tool = WebsiteSearchTool(
        url="https://www.booking.com",
        search_terms="flights from your city to user's destination"
    )

    # Define agents
    tourist_searcher = Agent(
        role="Tourist Place Researcher",
        goal="Find and summarize the top tourist places in Pakistan based on user interests.",
        tools=[search_tool, scrape_tool],
        verbose=True,
        backstory="A web search expert, proficient in finding the most exciting tourist spots based on the user's interests."
    )

    flight_finder = Agent(
        role="Flight Search Expert",
        goal="Find flights to top tourist spots in Pakistan within the user's budget.",
        tools=[search_tool, scrape_tool, flight_tool],
        verbose=True,
        memory=True,
        backstory="A dedicated travel expert skilled in finding the best flight options within the user's budget."
    )

    hotel_finder = Agent(
        role="Hotel Search Expert",
        goal="Find hotels near tourist destinations based on user preferences and budget.",
        tools=[search_tool, scrape_tool],
        verbose=True,
        memory=True,
        backstory="A travel expert proficient in finding the best hotels based on location, budget, and reviews."
    )

    restaurant_finder = Agent(
        role="Restaurant Search Expert",
        goal="Find the best restaurants near tourist spots based on user preferences (cuisine, price).",
        tools=[search_tool, scrape_tool],
        verbose=True,
        memory=True,
        backstory="An expert food guide with the ability to find restaurants based on cuisine preferences, ratings, and budget."
    )

    # Define tasks
    tourist_search_task = Task(
        description=f"Search the web for top tourist places in {inputs_details.search_query} based on the user's {inputs_details.interest}.",
        expected_output=f"A summary of the top tourist destinations in {inputs_details.search_query} based on the user's {inputs_details.interest} and {inputs_details.duration}.",
        agent=tourist_searcher
    )

    flight_search_task = Task(
        description=f"Search for flights in {inputs_details.search_query} based on user {inputs_details.budget}.",
        expected_output=f"List of {inputs_details.flight_search} flights to major tourist destinations, including airline names, times, prices (within user's {inputs_details.budget}).",
        agent=flight_finder
    )

    hotel_search_task = Task(
        description=f"Search for {inputs_details.hotel_search} near the tourist destination based on user preferences (location, price range, and duration).",
        expected_output=f"List of {inputs_details.hotel_search} near the tourist destination with ratings, prices, and booking links.",
        agent=hotel_finder
    )

    restaurant_search_task = Task(
        description=f"Find {inputs_details.restaurant_search} near the tourist destination, based on user preferences (cuisine, price).",
        expected_output=f"List of nearby {inputs_details.restaurant_search} with reviews, price ranges, and cuisine type.",
        agent=restaurant_finder
    )

    # Run each task individually and log the results
    tasks = [tourist_search_task, flight_search_task, hotel_search_task, restaurant_search_task]
    individual_results = []
    for task in tasks:
        logging.info(f"Starting task: {task.description}")
        try:
            task_result = task.execute()
            logging.info(f"Task completed: {task.description}")
            individual_results.append(TaskOutput(task_description=task.description, task_output=task_result))
        except Exception as e:
            logging.error(f"Error in task {task.description}: {str(e)}")

    # Combine results from individual tasks
    combined_output = "\n\n".join([result.task_output for result in individual_results])

    crew_result = CrewResult(
        combined_output=combined_output,
        tasks_output=individual_results,
        individual_task_results=individual_results
    )

    logging.info("Processing completed")
    return crew_result