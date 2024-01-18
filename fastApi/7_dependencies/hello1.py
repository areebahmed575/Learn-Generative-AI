# Global:
# When you define your top-level FastAPI application object, you can add dependen‐
# cies to it that will apply to all its path functions,

from fastapi import FastAPI, Depends 
def depfunc1():
    pass
def depfunc2(): 
    pass
app = FastAPI(dependencies=[Depends(depfunc1), Depends(depfunc2)])

@app.get("/main") 
def get_main():
    pass

# In this case, you’re using pass to ignore the other details to show how to attach the
# dependencies.

