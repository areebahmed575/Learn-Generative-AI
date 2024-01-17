from fastapi import FastAPI

app : FastAPI = FastAPI()

@app.get("/hi") 
def greet():
    return "Hello? World?"

@app.get("/hi/{who}")
def greet(who:str):
    return f"Hello? {who}?"



# @app.get("/hi/{name}")
# def greet_name(name:str):
#     return f"Hello {name}"

# @app.get("/hi/{name}/org/{organization}")
# def organization(name:str,organization:str):
#     return {"Name" :name, "Organization": organization} 


