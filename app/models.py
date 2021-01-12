from pydantic import BaseModel

import datetime


class BaseTask(BaseModel):
    title: str
    description: str


class CreateTask(BaseTask):
    pass


class Task(BaseTask):
    task_id: int
    date: datetime.datetime
    status: str
