from model import Creature

dragon = Creature(
    name="dragon",
    description=["incorrect", "string", "list"], #Try assigning a value of the wrong type to one or more of the Creature fields.
    country="*" ,
    area="*",
    aka="firedrake")


# Try assigning a value of the wrong type to one or more of the Creature fields.
#for run --> python test.py