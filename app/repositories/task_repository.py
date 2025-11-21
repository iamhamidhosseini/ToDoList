from typing import List, Optional
from datetime import datetime
from sqlalchemy import and_
from app.models.task import Task, TaskStatus
from app.models.project import Project
from app.repositories.base import BaseRepository
from app.exceptions.repository_exceptions import TaskNotFoundException, ProjectNotFoundException, DuplicateTaskException

class TaskRepository(BaseRepository[Task]):
    def get_by_id(self, id: str) -> Optional[Task]:
        return self.session.query(Task).filter(Task.id == id).first()
    
    def get_by_title_and_project(self, title: str, project_id: str) -> Optional[Task]:
        return self.session.query(Task).filter(
            Task.title == title,
            Task.project_id == project_id
        ).first()
    
    def get_all(self) -> List[Task]:
        return self.session.query(Task).order_by(Task.created_at).all()
    
    def get_by_project_id(self, project_id: str) -> List[Task]:
        return self.session.query(Task).filter(Task.project_id == project_id).order_by(Task.created_at).all()
    
    def create(self, task: Task) -> Task:
        # Verify project exists
        project = self.session.query(Project).filter(Project.id == task.project_id).first()
        if not project:
            raise ProjectNotFoundException(f"Project with id '{task.project_id}' not found")
        
        # Check for duplicate task title in same project
        existing = self.get_by_title_and_project(task.title, task.project_id)
        if existing:
            raise DuplicateTaskException(f"Task with title '{task.title}' already exists in this project")
        
        self.session.add(task)
        self.commit()
        self.refresh(task)
        return task
    
    def update(self, task: Task) -> Task:
        self.session.add(task)
        self.commit()
        self.refresh(task)
        return task
    
    def delete(self, id: str) -> bool:
        task = self.get_by_id(id)
        if not task:
            raise TaskNotFoundException(f"Task with id '{id}' not found")
        
        self.session.delete(task)
        self.commit()
        return True
    
    def count_by_project(self, project_id: str) -> int:
        from sqlalchemy import func
        return self.session.query(func.count(Task.id)).filter(Task.project_id == project_id).scalar()
    
    def get_overdue_tasks(self) -> List[Task]:
        return self.session.query(Task).filter(
            and_(
                Task.deadline < datetime.utcnow(),
                Task.status != TaskStatus.DONE
            )
        ).all()
    
    def close_overdue_tasks(self) -> int:
        overdue_tasks = self.get_overdue_tasks()
        closed_count = 0
        
        for task in overdue_tasks:
            task.mark_closed()
            self.session.add(task)
            closed_count += 1
        
        if closed_count > 0:
            self.commit()
        
        return closed_count
