from fastapi import FastAPI

app = FastAPI()

tasks = [{
    "id": 1,
    "title": "Estudar FastAPI",
    "completed": False
}]


@app.get("/tasks")
async def get_tasks():
    return tasks