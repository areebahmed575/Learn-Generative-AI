from model import Creature
from fastapi import FastAPI

app = FastAPI()

@app.get("/creature")
def get_all() -> list[Creature]:
    from data import get_creatures
    return get_creatures()

# FastAPI and Starlette automatically convert the original Creature model object list
# into a JSON string. This is the default output format in FastAPI, so we don’t need to
# specify it.