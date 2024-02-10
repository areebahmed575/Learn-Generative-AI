from openai.types.beta.threads import Run
from openai.types.beta.thread import Thread
from openai.types.beta.assistant import Assistant
from openai.types.beta.assistant_create_params import Tool
import time
import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import streamlit as st
from typing import Literal

from functions import available_functions


_: bool = load_dotenv(find_dotenv())  # read local .env file

client: OpenAI = OpenAI()

class Trip:
    def __init__(self, model: str = "gpt-3.5-turbo-1106"):
        self.client = OpenAI()
        self.model = model
        self.assistant: Assistant | None = None
        self.thread: Thread | None = None
        self.run: Run | None = None

