import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("Todo App")

def create_todo():
    title = st.text_input("Enter Todo Title")
    description = st.text_area("Enter Todo Description")
    if st.button("Add Todo"):
        response = requests.post(f"{BASE_URL}/todos/", json={"title": title, "description": description})
        if response.status_code == 200:
            st.success("Todo added successfully")

def delete_todo():
    todo_id = st.number_input("Enter Todo ID to delete")
    if st.button("Delete Todo"):
        response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
        if response.status_code == 200:
            st.success("Todo deleted successfully")

if __name__ == "__main__":
    create_todo()
    delete_todo()