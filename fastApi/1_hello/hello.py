from fastapi import FastAPI

app :FastAPI= FastAPI()

# @app.get("/")
# def index()->str:
#     return {"message":"Hello World"}

@app.get("/")
def index()->str:
    return "Pakistan Zindabad"


# to run -->uvicorn hello:app
#  to run -->http http://127.0.0.1:8000/
#  to run -->uvicorn hello:app --reload for update server
# http://127.0.0.1:8000/docs  --> for documentation