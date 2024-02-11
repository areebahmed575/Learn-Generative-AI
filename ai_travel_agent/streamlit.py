import streamlit as st
import os
import plotly.graph_objects as go
from assistant import Trip
from functions import tools,SEED_INSTRUCTION


MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_TOKEN")



st.set_page_config(
    page_title="AI Travel Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.header("AI Travel Assistant")


ai_travel : Trip = Trip()


ai_travel_assistant = ai_travel.create_assistant(
    name="AI Travel Assistant",
    instructions=SEED_INSTRUCTION,
    tools=tools,
)


ai_travel_thread = ai_travel.create_thread()

