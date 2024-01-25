from fastapi import FastAPI, status, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal
import models

app = FastAPI()

db = SessionLocal()

class OurBaseModel(BaseModel):
    class Config: # Config class is used to configure various settings for a model.
        from_attributes = True 

class Todo(OurBaseModel):
    message: str
    status: bool

@app.get('/', status_code=status.HTTP_200_OK)
def getAll_Todo():
    # Get all Todos from the database
    getAllTodo = db.query(models.Todo).all()
    return getAllTodo


@app.get('/getbyid/{todo_id}', response_model=Todo, status_code=status.HTTP_200_OK)
def get_Single_Todo(todo_id: int):
    # Get a single Todo from the database by their ID
    get_Todos = db.query(models.Todo).filter(
        models.Todo.id == todo_id).first()
    if get_Todos is not None:
        return get_Todos
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Todo not found")

@app.post('/addTodo', response_model=Todo, status_code=status.HTTP_201_CREATED)
def addTodo(todo: Todo):
    newTodo = models.Todo(message=todo.message, status=todo.status)
    db.add(newTodo)
    db.commit()

    return newTodo

@app.put('/update_todo/{todo_id}', status_code=status.HTTP_202_ACCEPTED)
def update_Todo(todo_id: int, todo: Todo):
    find_Todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if find_Todo is not None:
        find_Todo.message = todo.message
        find_Todo.status = todo.status

        db.commit()
        return find_Todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Todo not found")

@app.delete('/delete_todo/{todo_id}', response_model=Todo, status_code=200)
def delete_Todo(todo_id: int):
    find_Todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id).first()
    if find_Todo is not None:
        db.delete(find_Todo)
        db.commit()
        return find_Todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Todo not found")



# status_code= status.HTTP_202_ACCEPTED: This status code indicates that the request has been accepted for processing, but the processing has not been completed yet. It's often used for asynchronous processing,
# status_code= status.HTTP_201_CREATED: This status code indicates that the request has been successfully fulfilled and a new resource has been created as a result of it. It's commonly used in POST requests where a new resource is created on the server based on the data provided in the request body.
# Use status_code=200 when the request has been successfully processed, and you want to return the requested resource or indicate a generic success response.





