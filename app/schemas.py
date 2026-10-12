from pydantic import BaseModel
from typing import Literal

Priority = Literal["baixa", "media", "alta"]

class TaskCreate(BaseModel):
    title: str
    completed: bool = False
    priority: Priority = "media"


class TaskUpdate(BaseModel):
    title: str
    completed: bool
    priority: Priority


class TaskUpdateStatus(BaseModel):
    completed: bool