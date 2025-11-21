from typing import List, Optional
from sqlalchemy import func
from app.models.project import Project
from app.repositories.base import BaseRepository
from app.exceptions.repository_exceptions import ProjectNotFoundException, DuplicateProjectException

class ProjectRepository(BaseRepository[Project]):
    def get_by_id(self, id: str) -> Optional[Project]:
        return self.session.query(Project).filter(Project.id == id).first()
    
    def get_by_name(self, name: str) -> Optional[Project]:
        return self.session.query(Project).filter(Project.name == name).first()
    
    def get_all(self) -> List[Project]:
        return self.session.query(Project).order_by(Project.created_at).all()
    
    def create(self, project: Project) -> Project:
        # Check for duplicate name
        existing = self.get_by_name(project.name)
        if existing:
            raise DuplicateProjectException(f"Project with name '{project.name}' already exists")
        
        self.session.add(project)
        self.commit()
        self.refresh(project)
        return project
    
    def update(self, project: Project) -> Project:
        # Check for duplicate name (excluding current project)
        existing = self.session.query(Project).filter(
            Project.name == project.name,
            Project.id != project.id
        ).first()
        
        if existing:
            raise DuplicateProjectException(f"Project with name '{project.name}' already exists")
        
        self.session.add(project)
        self.commit()
        self.refresh(project)
        return project
    
    def delete(self, id: str) -> bool:
        project = self.get_by_id(id)
        if not project:
            raise ProjectNotFoundException(f"Project with id '{id}' not found")
        
        self.session.delete(project)
        self.commit()
        return True
    
    def count(self) -> int:
        return self.session.query(func.count(Project.id)).scalar()
    
    def project_exists(self, name: str) -> bool:
        return self.session.query(Project).filter(Project.name == name).first() is not None
