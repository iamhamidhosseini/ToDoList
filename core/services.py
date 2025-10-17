from typing import List, Optional
import uuid
from core.entities import Project, Task, TaskStatus
from storage.memory import MemoryStorage
from config import Config

class ProjectService:
    def __init__(self, storage: MemoryStorage):
        self.storage = storage
    
    def get_project_by_name(self, name: str):
        for project in self.storage.projects.values():
            if project.name == name:
                return project
        return None
    
    def create_project(self, name: str, description: str) -> tuple[bool, str]:
        if len(name) > Config.MAX_PROJECT_NAME_LENGTH:
            return False, f"Project name cannot exceed {Config.MAX_PROJECT_NAME_LENGTH} characters"
        
        if len(description) > Config.MAX_PROJECT_DESCRIPTION_LENGTH:
            return False, f"Project description cannot exceed {Config.MAX_PROJECT_DESCRIPTION_LENGTH} characters"
        
        if len(self.storage.projects) >= Config.MAX_NUMBER_OF_PROJECTS:
            return False, f"Cannot exceed maximum number of projects: {Config.MAX_NUMBER_OF_PROJECTS}"
        
        if self.storage.project_exists(name):
            return False, "Project with this name already exists"
        
        project = Project(
            id=str(uuid.uuid4()),
            name=name,
            description=description
        )
        self.storage.add_project(project)
        return True, "Project created successfully"
    
    def edit_project(self, project_name: str, new_name: str, description: str) -> tuple[bool, str]:
        project = self.get_project_by_name(project_name)
        
        if not project:
            return False, "Project not found"
        
        if len(new_name) > Config.MAX_PROJECT_NAME_LENGTH:
            return False, f"Project name cannot exceed {Config.MAX_PROJECT_NAME_LENGTH} characters"
        
        if len(description) > Config.MAX_PROJECT_DESCRIPTION_LENGTH:
            return False, f"Project description cannot exceed {Config.MAX_PROJECT_DESCRIPTION_LENGTH} characters"
        
        if new_name != project.name and self.storage.project_exists(new_name):
            return False, "Project with this name already exists"
        
        success = self.storage.update_project(project.id, new_name, description)
        return success, "Project updated successfully" if success else "Failed to update project"
    
    def delete_project(self, project_name: str) -> tuple[bool, str]:
        project = self.get_project_by_name(project_name)
        
        if not project:
            return False, "Project not found"
        
        success = self.storage.delete_project(project.id)
        return success, "Project deleted successfully" if success else "Project not found"
    
    def list_projects(self) -> List[Project]:
        return self.storage.get_all_projects()

class TaskService:
    def __init__(self, storage: MemoryStorage):
        self.storage = storage
        self.project_service = ProjectService(storage)
    
    def get_task_by_title(self, project_name: str, task_title: str):
        project = self.project_service.get_project_by_name(project_name)
        if not project:
            return None
        
        return self.storage.get_task_by_title(project.id, task_title)
    
    def create_task(self, project_name: str, title: str, description: str) -> tuple[bool, str]:
        project = self.project_service.get_project_by_name(project_name)
        
        if not project:
            return False, "Project not found"
        
        if len(title) > Config.MAX_TASK_TITLE_LENGTH:
            return False, f"Task title cannot exceed {Config.MAX_TASK_TITLE_LENGTH} characters"
        
        if len(description) > Config.MAX_TASK_DESCRIPTION_LENGTH:
            return False, f"Task description cannot exceed {Config.MAX_TASK_DESCRIPTION_LENGTH} characters"
        
        project_tasks = self.storage.get_project_tasks(project.id)
        if len(project_tasks) >= Config.MAX_NUMBER_OF_TASKS:
            return False, f"Cannot exceed maximum number of tasks per project: {Config.MAX_NUMBER_OF_TASKS}"
        
        task = Task(
            id=str(uuid.uuid4()),
            project_id=project.id,
            title=title,
            description=description,
            status=TaskStatus.TODO
        )
        self.storage.add_task(task)
        return True, "Task created successfully"
    
    def edit_task(self, project_name: str, task_title: str, new_title: str, description: str, status: str) -> tuple[bool, str]:
        task = self.get_task_by_title(project_name, task_title)
        if not task:
            return False, "Task not found"
        
        if len(new_title) > Config.MAX_TASK_TITLE_LENGTH:
            return False, f"Task title cannot exceed {Config.MAX_TASK_TITLE_LENGTH} characters"
        
        if len(description) > Config.MAX_TASK_DESCRIPTION_LENGTH:
            return False, f"Task description cannot exceed {Config.MAX_TASK_DESCRIPTION_LENGTH} characters"
        
        try:
            task_status = TaskStatus(status)
        except ValueError:
            return False, "Invalid status. Must be one of: todo, doing, done"
        
        success = self.storage.update_task(task.id, new_title, description, task_status)
        return success, "Task updated successfully" if success else "Failed to update task"
    
    def delete_task(self, project_name: str, task_title: str) -> tuple[bool, str]:
        task = self.get_task_by_title(project_name, task_title)
        if not task:
            return False, "Task not found"
        
        success = self.storage.delete_task(task.id)
        return success, "Task deleted successfully" if success else "Task not found"
    
    def list_project_tasks(self, project_name: str) -> tuple[bool, str | List[Task]]:
        project = self.project_service.get_project_by_name(project_name)
        
        if not project:
            return False, "Project not found"
        
        tasks = self.storage.get_project_tasks(project.id)
        return True, tasks
