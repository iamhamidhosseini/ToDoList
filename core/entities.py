from dataclasses import dataclass
from enum import Enum
from typing import Optional
import uuid
from datetime import datetime

class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

@dataclass
class Task:
    id: str
    project_id: str
    title: str
    description: str
    status: TaskStatus
    deadline: Optional[datetime] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class Project:
    id: str
    name: str
    description: str
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
