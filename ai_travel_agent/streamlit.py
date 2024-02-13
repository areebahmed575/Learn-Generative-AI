import streamlit as st
import os
import plotly.graph_objects as go
from assistant import Trip
from functions import tools,INSTRUCTION
from time import sleep


MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_TOKEN")



st.set_page_config(
    page_title="AI Travel Assistant",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.header("AI Travel Assistant🗺️✈️")


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
        "latitude": 24.8607,  
        "longitude": 67.0011,  
        "zoom": 12,  
    }

if "markers_state" not in st.session_state:
    st.session_state.markers_state = None

if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = []


def on_text_input():
    
    if st.session_state.input_user_msg == "":
        return
    
    st.session_state.conversation_state.append(
        ("user",st.session_state.input_user_msg)
    )

    ai_travel.add_message_to_thread(
        content=st.session_state.input_user_msg,
        role = "user"
    )
    with st.spinner('Fetching your traveling insights...'):  # Displaying the spinner
        # Simulate some processing time (you can replace this with your actual processing logic)
        sleep(2)

        run = ai_travel.create_run(
           instructions=INSTRUCTION
        )

        final_res = ai_travel.get_run_result(
          run=run,
          thread=thread
        )

    st.session_state.conversation_state = [
        (m.role, m.content[0].text.value)
        for m in reversed(final_res.data)
        
    ]
    




left_col,right_col = st.columns(2)


with left_col:
    
    st.button("Clear Conversation", on_click=lambda: st.session_state.conversation_state.clear())
    for role,message in st.session_state.conversation_state:
        with st.chat_message(role):
            st.write(message)

with right_col:
    figure = go.Figure(go.Scattermapbox(
        mode="markers",
    ))
    if st.session_state.markers_state is not None:# it implies that there is marker data available, so you can proceed with plotting the markers based on the available data.
        figure.add_trace(
            go.Scattermapbox(
                mode="markers",
                marker=dict(
                    symbol='marker',
                    size=10,  
                    color='blue',  
                    opacity=0.8,
                ),
                lat=st.session_state.markers_state["latitudes"],
                lon=st.session_state.markers_state["longitudes"],
                text=st.session_state.markers_state["labels"],
                customdata=st.session_state.markers_state.get("altitudes", []),
                hovertemplate=(
                    "<b>%{text}</b><br>" +
                    "Latitude: %{lat}<br>" +
                    "Longitude: %{lon}<br>" +
                    "Altitude: %{customdata}<extra></extra>"
                )
            )
        )
    figure.update_layout(
        mapbox=dict(
            accesstoken=MAPBOX_ACCESS_TOKEN,
            center=go.layout.mapbox.Center(
                lat=st.session_state.map["latitude"],
                lon=st.session_state.map["longitude"]
            ),
            zoom=st.session_state.map["zoom"]
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,  
    )

    st.plotly_chart(
        figure,
        config={"displayModeBar": False},
        use_container_width=True,
        key="plotly"
    )




st.chat_input(
    placeholder="What are three must-visit places in New York City that are situated close to each other and suitable for exploring in December?",
    key="input_user_msg",
    on_submit=on_text_input
)



