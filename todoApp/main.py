from fastapi import FastAPI, status, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal
import models

app = FastAPI()

db = SessionLocal()

class OurBaseModel(BaseModel):
    class Config:
        from_attributes = True

class Todo(OurBaseModel):
    message: str
    status: bool

@app.post('/addTodo', response_model=Todo, status_code=status.HTTP_201_CREATED)
def addTodo(todo: Todo):
    newTodo = models.Todo(message=todo.message, status=todo.status)
    db.add(newTodo)
    db.commit()

    return newTodo


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
