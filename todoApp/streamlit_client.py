import streamlit as st
import requests


BASE_URL = "http://127.0.0.1:8000"

st.title("Todo App")

def createtodo():
    st.markdown("Create Todo")      
    title = st.text_input(
        "Enter New Todo", placeholder="Read Book before Sleep") 
    convert_str = str(title)  
    if st.button("Add Todo"):  
        if title: 
            response = requests.post(f"{BASE_URL}/addTodo", json={"message": convert_str, "status": False})
            st.success("Added Todo Successfully")  




def delete_todo():
    st.markdown("Delete Todo")
    todo_id = st.number_input(
        "Enter Todo ID to delete", step=1)  
    todo_id = int(todo_id)  
    if st.button("Delete Todo"):  
        response = requests.delete(f"{BASE_URL}/delete_todo/{todo_id}")
        st.warning("Deleted Todo Succesfully!")
            

if __name__ == "__main__":
    createtodo()
    delete_todo()