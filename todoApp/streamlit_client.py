import streamlit as st
import requests


BASE_URL = "http://127.0.0.1:8000"

st.title("Todo App")

def createtodo():
    st.markdown("Create Todo")      
    title = st.text_input(
        "Enter New Todo", placeholder="Paying bills") 
    convert_str = str(title)  
    if st.button("Add Todo"):  
        if title: 
            response = requests.post(f"{BASE_URL}/addTodo", json={"message": convert_str, "status": False})
            st.success("Added Todo Successfully")  

def update_todo():
    st.markdown("Update Todo")  
    todo_id = st.number_input("Enter Todo ID to Edit",step=1, min_value=0) 
    message = st.text_input("Enter Todo", placeholder="Updating financial records")
    status = st.radio("Enter Status", ('False', 'True'))  
    status = True if status == 'True' else False 

    data = {
        "id": todo_id,
        "message": message,
        "status": status
    }  

    if st.button("Edit Todo"): 
        url = f"http://127.0.0.1:8000/update_todo/{todo_id}"
        response = requests.put(url, json=data)  
        if response:  
            st.success("Todo Updated Successfully")  
        else:  
            st.error(
                f"PUT request failed with status code: {response.status_code}")  
            print(response.text)



    


def delete_todo():
    st.markdown("Delete Todo")
    todo_id = st.number_input(
        "Enter Todo ID to delete", step=1, min_value=0)  # Set min_value to 0
    todo_id = int(todo_id)
    if st.button("Delete Todo"):
        response = requests.delete(f"{BASE_URL}/delete_todo/{todo_id}")
        st.warning("Deleted Todo Successfully!")

         

def show_todo(): 
    st.markdown("Here is your Todos List")
    
    response = requests.get("http://127.0.0.1:8000/")
    todos = response.json()
    table_data = []

    for todo in todos:
        table_data.append([todo['id'], todo['message'], todo['status']])

    # Add header row
    table_data.insert(0, ['id', 'message', 'status'])
   
    st.table(table_data)




if __name__ == "__main__":
    createtodo()
    update_todo()
    delete_todo()
    show_todo()
   