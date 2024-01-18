from pydantic import BaseModel

class Creature(BaseModel):
    name: str
    country: str
    area: str
    description: str
    aka: str


thing = Creature(
    name="yeti",
    country="CN",
    area="Himalayas",
    description="Hirsute Himalayan",
    aka="Abominable Snowman")

print("Name is", thing.name)

# Models are the best way to define data that will be passed around in your web appli‐
# cation. Pydantic leverages Python’s type hints to define data models to pass around in
# your application. 