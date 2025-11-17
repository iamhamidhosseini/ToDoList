from typing import List, Optional, Tuple
import uuid
from datetime import datetime

from .entities import Project, Task, TaskStatus
from storage.memory import MemoryStorage
from config import Config

class ProjectService:
    def __init__(self, storage: MemoryStorage):
        self.storage = storage
    
    def get_project_by_name(self, name: str) -> Optional[Project]:
        for project in self.storage.projects.values():
            if project.name == name:
                return project
        return None
    
    def get_project_by_id(self, project_id: str) -> Optional[Project]:
        return self.storage.get_project(project_id)
    
    def create_project(self, name: str, description: str) -> Tuple[bool, str]:
        if not name.strip():
            return False, "Project name cannot be empty"
        
        if len(name) > Config.MAX_PROJECT_NAME_LENGTH:
            return False, Config.get_validation_message("Project name", Config.MAX_PROJECT_NAME_LENGTH)
        
        if len(description) > Config.MAX_PROJECT_DESCRIPTION_LENGTH:
            return False, Config.get_validation_message("Project description", Config.MAX_PROJECT_DESCRIPTION_LENGTH)
        
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
    
    def edit_project(self, project_name: str, new_name: str, description: str) -> Tuple[bool, str]:
        project = self.get_project_by_name(project_name)
        
        if not project:
            return False, "Project not found"
        
        if not new_name.strip():
            return False, "Project name cannot be empty"
        
        if len(new_name) > Config.MAX_PROJECT_NAME_LENGTH:
            return False, Config.get_validation_message("Project name", Config.MAX_PROJECT_NAME_LENGTH)
        
        if len(description) > Config.MAX_PROJECT_DESCRIPTION_LENGTH:
            return False, Config.get_validation_message("Project description", Config.MAX_PROJECT_DESCRIPTION_LENGTH)
        
        if new_name != project.name and self.storage.project_exists(new_name):
            return False, "Project with this name already exists"
        
        project.update_details(new_name, description)
        success = self.storage.update_project(project.id, new_name, description)
        return success, "Project updated successfully" if success else "Failed to update project"
    
    def delete_project(self, project_name: str) -> Tuple[bool, str]:
        project = self.get_project_by_name(project_name)
        
        if not project:
            return False, "Project not found"
        
        success = self.storage.delete_project(project.id)
        return success, "Project deleted successfully" if success else "Failed to delete project"
    
    def list_projects(self) -> List[Project]:
        return self.storage.get_all_projects()

class TaskService:
    def __init__(self, storage: MemoryStorage, project_service: ProjectService):
        self.storage = storage
        self.project_service = project_service
    
    def get_task_by_title(self, project_name: str, task_title: str) -> Optional[Task]:
        project = self.project_service.get_project_by_name(project_name)
        if not project:
            return None
        
        return self.storage.get_task_by_title(project.id, task_title)
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        return self.storage.get_task(task_id)
    
    def create_task(self, project_name: str, title: str, description: str, deadline: Optional[datetime] = None) -> Tuple[bool, str]:
        project = self.project_service.get_project_by_name(project_name)
        
        if not project:
            return False, "Project not found"
        
        # Validation
        if not title.strip():
            return False, "Task title cannot be empty"
        
        if len(title) > Config.MAX_TASK_TITLE_LENGTH:
            return False, Config.get_validation_message("Task title", Config.MAX_TASK_TITLE_LENGTH)
        
        if len(description) > Config.MAX_TASK_DESCRIPTION_LENGTH:
            return False, Config.get_validation_message("Task description", Config.MAX_TASK_DESCRIPTION_LENGTH)
        
        project_tasks = self.storage.get_project_tasks(project.id)
        if len(project_tasks) >= Config.MAX_NUMBER_OF_TASKS:
            return False, f"Cannot exceed maximum number of tasks per project: {Config.MAX_NUMBER_OF_TASKS}"
        
        # Create task
        task = Task(
            id=str(uuid.uuid4()),
            project_id=project.id,
            title=title,
            description=description,
            status=TaskStatus.TODO,
            deadline=deadline
        )
        self.storage.add_task(task)
        return True, "Task created successfully"
    
    def edit_task(self, project_name: str, task_title: str, new_title: str, description: str, status: str) -> Tuple[bool, str]:
        """Edit an existing task"""
        task = self.get_task_by_title(project_name, task_title)
        if not task:
            return False, "Task not found"
        
        # Validation
        if not new_title.strip():
            return False, "Task title cannot be empty"
        
        if len(new_title) > Config.MAX_TASK_TITLE_LENGTH:
            return False, Config.get_validation_message("Task title", Config.MAX_TASK_TITLE_LENGTH)
        
        if len(description) > Config.MAX_TASK_DESCRIPTION_LENGTH:
            return False, Config.get_validation_message("Task description", Config.MAX_TASK_DESCRIPTION_LENGTH)
        
        try:
            task_status = TaskStatus(status)
        except ValueError:
            return False, "Invalid status. Must be one of: todo, doing, done"
        
        # Update task
        success = task.update_details(new_title, description, status)
        if success:
            storage_success = self.storage.update_task(task.id, new_title, description, task_status)
            return storage_success, "Task updated successfully" if storage_success else "Failed to update task in storage"
        return False, "Failed to update task details"
    
    def delete_task(self, project_name: str, task_title: str) -> Tuple[bool, str]:
        task = self.get_task_by_title(project_name, task_title)
        if not task:
            return False, "Task not found"
        
        success = self.storage.delete_task(task.id)
        return success, "Task deleted successfully" if success else "Failed to delete task"
    
    def change_task_status(self, project_name: str, task_title: str, status: str) -> Tuple[bool, str]:
        """Change task status"""
        task = self.get_task_by_title(project_name, task_title)
        if not task:
            return False, "Task not found"
        
        try:
            task_status = TaskStatus(status)
        except ValueError:
            return False, "Invalid status. Must be one of: todo, doing, done"
        
        success = task.change_status(status)
        if success:
            storage_success = self.storage.update_task(task.id, task.title, task.description, task_status)
            return storage_success, f"Task status changed to {status}" if storage_success else "Failed to update task status in storage"
        return False, "Failed to change task status"
    
    def list_project_tasks(self, project_name: str) -> Tuple[bool, str | List[Task]]:
        """Get all tasks for a project"""
        project = self.project_service.get_project_by_name(project_name)
        
        if not project:
            return False, "Project not found"
        
        tasks = self.storage.get_project_tasks(project.id)
        return True, tasks
    
    def list_all_tasks(self) -> List[Task]:
        """Get all tasks across all projects"""
        all_tasks = []
        for project_id in self.storage.project_tasks:
            tasks = self.storage.get_project_tasks(project_id)
            all_tasks.extend(tasks)
        return all_tasks
