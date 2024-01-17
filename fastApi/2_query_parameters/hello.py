# query_parameters
from fastapi import FastAPI

app : FastAPI = FastAPI()


# @app.get("/notifications/")
# def notifications(filter:str):
#     #return {"data" :  "filter " +  filter} 
#     return {"data" : f"filter {filter}"} 
# #http://127.0.0.1:8000/notifications/?filter=areeb

@app.get("/hi/") 
def greet(who):
    return f"Hello? {who}?"
#localhost:8000/hi?who=Mom

# print(__name__)

if __name__ == "__main__": 
    import uvicorn
    uvicorn.run("hello:app", reload=True)