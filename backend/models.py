from datetime import datetime
from enum import Enum
from dataclasses import dataclass

from pydantic import BaseModel, UUID4, validator


class TaskImportance(Enum):
    LOW = "low"
    BASIC = "basic"
    IMPORTANT = "important"


class Task(BaseModel):
    # Main fields
    id: UUID4
    title: str
    description: str
    done: bool
    tags: list[str]
    created_at: datetime
    changed_at: datetime

    # Optional fields
    importance: TaskImportance = TaskImportance.BASIC
    deadline: datetime | None = None
    color: str | None = None

    @validator('created_at', 'changed_at', 'deadline', pre=True)
    def convert_timestamp(cls, v):
        if isinstance(v, int):
            try:
                return datetime.fromtimestamp(v)
            except TypeError:
                raise ValueError('invalid value of unix timestamp')
        return v


class Tasks(BaseModel):
    list: list[Task]
    revision: int


@dataclass
class UserInfo:
    id: str
    psuid: str
    client_id: str
    login: str

    display_name: str
    real_name: str
    first_name: str
    last_name: str
    sex: str

    default_avatar_id: str
    is_avatar_empty: bool
