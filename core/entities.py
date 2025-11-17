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
    
    def change_status(self, new_status: str) -> bool:
        try:
            self.status = TaskStatus(new_status)
            return True
        except ValueError:
            return False
    
    def update_details(self, title: str, description: str, status: str) -> bool:
        if not title.strip():
            return False
        
        self.title = title
        self.description = description
        return self.change_status(status)
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        deadline = None
        if data.get('deadline'):
            deadline = datetime.fromisoformat(data['deadline'])
        
        created_at = datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        
        return cls(
            id=data['id'],
            project_id=data['project_id'],
            title=data['title'],
            description=data['description'],
            status=TaskStatus(data['status']),
            deadline=deadline,
            created_at=created_at
        )

@dataclass
class Project:
    id: str
    name: str
    description: str
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def update_details(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        created_at = datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            created_at=created_at
        )
