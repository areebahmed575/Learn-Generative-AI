import requests

BASE_URL = "http://127.0.0.1:8000"

def create_todo():
    title = input("Enter Todo Title: ")
    description = input("Enter Todo Description: ")
    response = requests.post(f"{BASE_URL}/todos/", json={"title": title, "description": description})
    if response.status_code == 200:
        print("Todo added successfully")

def delete_todo():
    todo_id = input("Enter Todo ID to delete: ")
    response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    if response.status_code == 200:
        print("Todo deleted successfully")

if __name__ == "__main__":
    create_todo()
    delete_todo()