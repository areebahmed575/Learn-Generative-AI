import streamlit as st
import os
import plotly.graph_objects as go
from assistant import Trip
from functions import tools,INSTRUCTION


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
    instructions=INSTRUCTION,
    tools=tools,
    file_obj=[],
)


thread = ai_travel.create_thread()



if "map" not in st.session_state:
    st.session_state.map = {
        "latitude": 39.949610,
        "longitude": -75.150282,
        "zoom": 16,
    }


if "markers_state" not in st.session_state:
    st.session_state = None

if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = []


def on_text_input():
    if st.session_state.input_user_msg == "":
        return
    
    st.session_state.conversation_state.append(
        ("user",st.session_state.input_user_msg)
    )

    ai_travel.add_message_to_thread(
        role = "user",
        content=st.session_state.input_user_msg
    )

    run = ai_travel.create_run(
        instructions=INSTRUCTION
    )

    final_res = ai_travel.get_run_result(
        run=run,
        thread=thread
    )

    st.session_state.conversation_state = [
        (m.role, m.content[0].text.value)
        for m in final_res.data
    ]



left_col,right_col = st.columns(2)


with left_col:
    for role,message in st.session_state.conversation_state:
        with st.chat(role):
            st.write(message)




st.chat_input(
    placeholder="Share 3 places in UAE nearby to each other I can visit in december holidays",
    key="input_user_msg",
    on_submit=on_text_input
)



