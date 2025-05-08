
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the InsTaG RunPod Agent"}

# More endpoints will be added here by the agent as it processes the tasks

