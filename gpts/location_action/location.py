from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated

app = FastAPI(title="Locaction Finder API", version="1.0.0")

class Location(BaseModel):
    name: str
    location: str

locations = {
    "zia": Location(name="Zia", location="Karachi"),
    "ali": Location(name="Ali", location="Lahore"),
}

# depency function
def get_location_or_404(name:str)->Location:
    loc = locations.get(name.lower())
    if not loc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No location found for {name}")
    return loc


@app.get("/location/{name}")
def get_person_location(name:str, location: Annotated[Location, Depends(get_location_or_404)]):
    return location

#http://127.0.0.1:8000/openapi.json
#open ai ko batana h k mairy api call krsktay h(action) tou aap yeh format call(open api->api specification)krsktay h