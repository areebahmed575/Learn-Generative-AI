from fastapi import FastAPI, Body

app :FastAPI =FastAPI()

@app.post("/hi")
def greet(who: str = Body(embed=True)):
    return {"message": f"Hello {who}"}

#That Body(embed=True) is needed to tell FastAPI that, this time, we get the value of who from the JSON-formatted 
#request body. The embed part means that it should look like {"who": "Mom"} rather than just "Mom".
