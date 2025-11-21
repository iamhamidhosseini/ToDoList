from sqlalchemy import Column, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.db.base import Base

class TaskStatus:
    TODO = "todo"
    DOING = "doing" 
    DONE = "done"

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus.TODO, TaskStatus.DOING, TaskStatus.DONE, 
                        name='task_status'), default=TaskStatus.TODO)
    deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    
    # Relationship with project
    project = relationship("Project", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None
        }
    
    def mark_closed(self):
        self.status = TaskStatus.DONE
        self.closed_at = datetime.utcnow()
    
    def is_overdue(self):
        if self.deadline and self.status != TaskStatus.DONE:
            return datetime.utcnow() > self.deadline
        return False
