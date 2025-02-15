from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import uvicorn
from langchain_core.messages import HumanMessage
from fastapi.middleware.cors import CORSMiddleware
from agent import graph  # Assuming this is your Langgraph agent
import json
import asyncio

class TravelPlanRequest(BaseModel):
    budget: float
    interests: List[str]
    companions: int
    city: str
    days: int
    travel_date: str
    initial_message: str = "Plan my trip to Pakistan"

app = FastAPI(title="Travel Planner API", description="API for generating travel itineraries using Langgraph.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/plan_trip")
async def plan_trip(request: TravelPlanRequest):
    try:
        # Build the initial state for your agent

        print("Received request:", request.dict())

        initial_state = {
            "messages": [HumanMessage(content=request.initial_message)],
            "budget": request.budget,
            "interests": request.interests,
            "companions": request.companions,
            "city": request.city,
            "days": request.days,
            "travel_date": request.travel_date,
            "itinerary": []  # This will be populated by your agent
        }

        # Optional configuration 
        config = {"configurable": {"thread_id": "1"}}

        # Use astream instead of invoke
        response = [chunk async for chunk in graph.astream(initial_state, config)]
        
        # Take the last chunk as the final response
        final_response = response[-1]

        print("Generated response:", final_response)
        
        return final_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating itinerary: {str(e)}")

if __name__ == "__main__":
    # Run the API using uvicorn on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)