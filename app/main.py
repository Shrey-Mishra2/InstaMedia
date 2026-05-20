from fastapi import FastAPI

app = FastAPI()

@app.get("/about")
def greetings():
    return {"nothing to see right now"}
