# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine
from pydantic import BaseModel
from assistant import Trip
from functions import tools, INSTRUCTION
import os

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the AI assistant
ai_travel = Trip()
ai_travel_assistant = ai_travel.create_assistant(
    name="AI Travel Assistant",
    instructions=INSTRUCTION,
    tools=tools,
    # Removed file_obj=[]
)
thread = ai_travel.create_thread()

# Pydantic model for user input
class UserMessage(BaseModel):
    message: str

@app.post("/chat")
async def chat(user_message: UserMessage):
    ai_travel.add_message_to_thread(
        content=user_message.message,
        role="user"
    )

    run = ai_travel.create_run(
        instructions=INSTRUCTION
    )

    final_res = ai_travel.get_run_result(
        run=run,
        thread=thread
    )

    # Extract assistant's response
    assistant_responses = [
        m.content[0].text.value
        for m in reversed(final_res["messages"].data)
        if m.role == "assistant"
    ]

    if assistant_responses:
        response_text = assistant_responses[0]
    else:
        response_text = "I'm sorry, I couldn't process your request."

    return {
        "response": response_text,
        "function_outputs": final_res["function_outputs"]
    }
