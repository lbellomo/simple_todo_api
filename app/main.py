from os import environ
import datetime

from fastapi import FastAPI, HTTPException

from app.shelve_db import ShelveDB
from app.models import CreateTask, Task

shelve_path = environ.get("SHELVE_PATH", "/tmp/shelve.db")

app = FastAPI()
shelve_db = ShelveDB(shelve_path)


@app.get("/task")
async def get_tasks():
    result = shelve_db.get_all()
    return {"message": "ok", "result": result}


@app.post("/task")
async def create_task(task: CreateTask):
    next_id = shelve_db.get_next_id()
    date = datetime.datetime.now()
    task = Task(
        task_id=next_id,
        status="Pending",
        title=task.title,
        description=task.description,
        date=date,
    )

    try:
        shelve_db.create(task, "task_id")
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid task_id")

    return {"message": "ok", "result": task}


@app.get("/task/{task_id}")
async def get_task(task_id: int):
    try:
        task = shelve_db.get(task_id)
    except KeyError:
        raise HTTPException(
            status_code=400, detail=f"Invalid task_id: 'task_id {task_id}' don't exist."
        )

    return {"message": "ok", "result": task}


@app.put("/task/{task_id}")
async def update_task(task_id: int, status: str = "Done"):
    status = status.strip().capitalize()

    if status not in ["Done", "Pending", "Cancel"]:
        raise HTTPException(
            status_code=400,
            detail="Query parameter 'status' invalid. Should be 'Done', 'Pending' or 'Cancel'",
        )

    try:
        task = shelve_db.get(task_id)
        task["status"] = status
        shelve_db.update(task_id, task)
    except KeyError:
        raise HTTPException(
            status_code=400, detail=f"Invalid task_id: 'task_id {task_id}' don't exist."
        )

    return {"message": "ok", "result": task}


@app.delete("/task/{task_id}")
async def delete_task(task_id: int):
    try:
        shelve_db.delete(task_id)
    except KeyError:
        raise HTTPException(
            status_code=400, detail=f"Invalid task_id: 'task_id {task_id}' don't exist."
        )

    return {"message": "ok"}
