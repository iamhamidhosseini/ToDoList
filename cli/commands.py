from datetime import datetime
from core.services import ProjectService, TaskService
from storage.memory import MemoryStorage

class CLICommands:
    def __init__(self, project_service: ProjectService, task_service: TaskService):
        self.project_service = project_service
        self.task_service = task_service
    
    def create_project(self, name: str, description: str):
        """Create a new project"""
        success, message = self.project_service.create_project(name, description)
        print(message)
    
    def edit_project(self, project_name: str, new_name: str, description: str):
        """Edit an existing project"""
        success, message = self.project_service.edit_project(project_name, new_name, description)
        print(message)
    
    def delete_project(self, project_name: str):
        """Delete a project"""
        success, message = self.project_service.delete_project(project_name)
        print(message)
    
    def list_projects(self):
        """List all projects"""
        projects = self.project_service.list_projects()
        if not projects:
            print("No projects found")
            return
        
        print("\n=== Projects ===")
        for project in projects:
            print(f"Name: {project.name}")
            print(f"Description: {project.description}")
            print(f"Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"ID: {project.id}")
            print("-" * 40)
    
    def create_task(self, project_name: str, title: str, description: str, deadline: str = None):
        """Create a new task"""
        deadline_obj = None
        if deadline:
            try:
                deadline_obj = datetime.strptime(deadline, '%Y-%m-%d')
            except ValueError:
                print("Invalid deadline format. Use YYYY-MM-DD.")
                return
        
        success, message = self.task_service.create_task(project_name, title, description, deadline_obj)
        print(message)
    
    def edit_task(self, project_name: str, task_title: str, new_title: str, description: str, status: str):
        success, message = self.task_service.edit_task(project_name, task_title, new_title, description, status)
        print(message)
    
    def delete_task(self, project_name: str, task_title: str):
        success, message = self.task_service.delete_task(project_name, task_title)
        print(message)
    
    def change_task_status(self, project_name: str, task_title: str, status: str):
        success, message = self.task_service.change_task_status(project_name, task_title, status)
        print(message)
    
    def list_tasks(self, project_name: str = None):
        if project_name:
            success, result = self.task_service.list_project_tasks(project_name)
            if not success:
                print(result)
                return
            
            if not result:
                print("No tasks found for this project")
                return
            
            print(f"\n=== Tasks for Project: {project_name} ===")
        else:
            result = self.task_service.list_all_tasks()
            if not result:
                print("No tasks found")
                return
            print("\n=== All Tasks ===")
        
        for task in result:
            status_icon = "✓" if task.status.value == "done" else "○" if task.status.value == "doing" else "✗"
            deadline = task.deadline.strftime("%Y-%m-%d") if task.deadline else "No deadline"
            print(f"[{status_icon}] {task.title} (Project: {self._get_project_name(task.project_id)})")
            print(f"   Description: {task.description}")
            print(f"   Status: {task.status.value}")
            print(f"   Due: {deadline}")
            print(f"   ID: {task.id}")
            print("-" * 40)
    
    def _get_project_name(self, project_id: str) -> str:
        project = self.project_service.get_project_by_id(project_id)
        return project.name if project else "Unknown Project"
