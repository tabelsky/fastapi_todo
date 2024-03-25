import datetime
from pydantic import BaseModel


class TodoItem(BaseModel):
    title: str
    description: str
    is_done: bool = False
    is_important: bool = False
    created_at: datetime.datetime
