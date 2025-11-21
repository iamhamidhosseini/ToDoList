from typing import List, Tuple
from app.models.project import Project
from app.repositories.project_repository import ProjectRepository
from app.exceptions.service_exceptions import ValidationException, BusinessRuleException
from app.exceptions.repository_exceptions import ProjectNotFoundException, DuplicateProjectException
from config import Config

class ProjectService:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository
    
    def create_project(self, name: str, description: str = "") -> Tuple[bool, str]:
        try:
            # Validation
            if not name.strip():
                raise ValidationException("Project name cannot be empty")
            
            if len(name) > Config.MAX_PROJECT_NAME_LENGTH:
                raise ValidationException(f"Project name cannot exceed {Config.MAX_PROJECT_NAME_LENGTH} characters")
            
            if len(description) > Config.MAX_PROJECT_DESCRIPTION_LENGTH:
                raise ValidationException(f"Project description cannot exceed {Config.MAX_PROJECT_DESCRIPTION_LENGTH} characters")
            
            if self.project_repository.count() >= Config.MAX_NUMBER_OF_PROJECTS:
                raise BusinessRuleException(f"Cannot exceed maximum number of projects: {Config.MAX_NUMBER_OF_PROJECTS}")
            
            # Create project
            project = Project(name=name, description=description)
            created_project = self.project_repository.create(project)
            
            return True, f"Project '{created_project.name}' created successfully"
        
        except (ValidationException, BusinessRuleException, DuplicateProjectException) as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def edit_project(self, project_id: str, name: str, description: str = "") -> Tuple[bool, str]:
        try:
            project = self.project_repository.get_by_id(project_id)
            if not project:
                raise ProjectNotFoundException("Project not found")
            
            # Validation
            if not name.strip():
                raise ValidationException("Project name cannot be empty")
            
            if len(name) > Config.MAX_PROJECT_NAME_LENGTH:
                raise ValidationException(f"Project name cannot exceed {Config.MAX_PROJECT_NAME_LENGTH} characters")
            
            if len(description) > Config.MAX_PROJECT_DESCRIPTION_LENGTH:
                raise ValidationException(f"Project description cannot exceed {Config.MAX_PROJECT_DESCRIPTION_LENGTH} characters")
            
            # Update project
            project.name = name
            project.description = description
            updated_project = self.project_repository.update(project)
            
            return True, f"Project '{updated_project.name}' updated successfully"
        
        except (ValidationException, BusinessRuleException, ProjectNotFoundException, DuplicateProjectException) as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def delete_project(self, project_id: str) -> Tuple[bool, str]:
        try:
            success = self.project_repository.delete(project_id)
            return True, "Project deleted successfully"
        
        except ProjectNotFoundException as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def list_projects(self) -> List[Project]:
        return self.project_repository.get_all()
    
    def get_project_by_id(self, project_id: str):
        return self.project_repository.get_by_id(project_id)
    
    def get_project_by_name(self, name: str):
        return self.project_repository.get_by_name(name)
