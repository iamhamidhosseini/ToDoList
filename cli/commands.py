from core.services import ProjectService, TaskService
from storage.memory import MemoryStorage

class CLICommands:
    def __init__(self):
        self.storage = MemoryStorage()
        self.project_service = ProjectService(self.storage)
        self.task_service = TaskService(self.storage)
    
    def create_project(self, name: str, description: str):
        success, message = self.project_service.create_project(name, description)
        print(message)
    
    def edit_project(self, project_name: str, new_name: str, description: str):
        success, message = self.project_service.edit_project(project_name, new_name, description)
        print(message)
    
    def delete_project(self, project_name: str):
        success, message = self.project_service.delete_project(project_name)
        print(message)
    
    def list_projects(self):
        projects = self.project_service.list_projects()
        if not projects:
            print("No projects found")
            return
        
        print("\n=== Projects ===")
        for project in projects:
            print(f"Name: {project.name}")
            print(f"Description: {project.description}")
            print(f"Created: {project.created_at}")
            print("-" * 40)
    
    def create_task(self, project_name: str, title: str, description: str):
        success, message = self.task_service.create_task(project_name, title, description)
        print(message)
    
    def edit_task(self, project_name: str, task_title: str, new_title: str, description: str, status: str):
        success, message = self.task_service.edit_task(project_name, task_title, new_title, description, status)
        print(message)
    
    def delete_task(self, project_name: str, task_title: str):
        success, message = self.task_service.delete_task(project_name, task_title)
        print(message)
    
    def list_tasks(self, project_name: str):
        success, result = self.task_service.list_project_tasks(project_name)
        if not success:
            print(result)
            return
        
        if not result:
            print("No tasks found for this project")
            return
        
        print(f"\n=== Tasks for Project: {project_name} ===")
        for task in result:
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Status: {task.status.value}")
            print(f"Created: {task.created_at}")
            print("-" * 40)
