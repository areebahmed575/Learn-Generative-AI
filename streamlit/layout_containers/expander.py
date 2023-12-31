#Insert a multi-element container that can be expanded/collapsed.

# Inserts a container into your app that can be used to hold multiple elements and can be expanded or collapsed by the user. When collapsed, all that is visible is the provided label. 
import streamlit as st

# st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

with st.expander("See explanation"):
    st.write("The chart above shows some numbers I picked for you. I rolled actual dice for these, so they're guaranteed to be random.")
    st.image("https://static.streamlit.io/examples/dice.jpg")