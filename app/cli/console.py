import click
from datetime import datetime
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository

class CLICommands:
    def __init__(self, project_service: ProjectService, task_service: TaskService):
        self.project_service = project_service
        self.task_service = task_service
    
    def display_project(self, project):
        print(f"Name: {project.name}")
        print(f"Description: {project.description}")
        print(f"Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"ID: {project.id}")
        print(f"Tasks: {len(project.tasks) if project.tasks else 0}")
        print("-" * 40)
    
    def display_task(self, task):
        status_icon = "✓" if task.status == "done" else "○" if task.status == "doing" else "✗"
        deadline = task.deadline.strftime("%Y-%m-%d") if task.deadline else "No deadline"
        closed_at = task.closed_at.strftime("%Y-%m-%d %H:%M") if task.closed_at else "Not closed"
        
        print(f"[{status_icon}] {task.title}")
        print(f"   Description: {task.description}")
        print(f"   Status: {task.status}")
        print(f"   Due: {deadline}")
        print(f"   Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Closed: {closed_at}")
        print(f"   ID: {task.id}")
        print("-" * 40)
    
    def create_project(self, name: str, description: str):
        success, message = self.project_service.create_project(name, description)
        print(message)
    
    def edit_project(self, project_name: str, new_name: str, description: str):
        project = self.project_service.get_project_by_name(project_name)
        if not project:
            print("Project not found")
            return
        
        success, message = self.project_service.edit_project(project.id, new_name, description)
        print(message)
    
    def delete_project(self, project_name: str):
        project = self.project_service.get_project_by_name(project_name)
        if not project:
            print("Project not found")
            return
        
        success, message = self.project_service.delete_project(project.id)
        print(message)
    
    def list_projects(self):
        projects = self.project_service.list_projects()
        if not projects:
            print("No projects found")
            return
        
        print(f"\n=== Projects ({len(projects)}) ===")
        for project in projects:
            self.display_project(project)
    
    def create_task(self, project_name: str, title: str, description: str, deadline: str = None):
        deadline_obj = None
        if deadline:
            try:
                deadline_obj = datetime.strptime(deadline, '%Y-%m-%d')
            except ValueError:
                print("Invalid deadline format. Use YYYY-MM-DD.")
                return
        
        success, message = self.task_service.create_task(project_name, title, description, deadline_obj)
        print(message)
    
    def edit_task(self, task_id: str, title: str, description: str, status: str):
        success, message = self.task_service.edit_task(task_id, title, description, status)
        print(message)
    
    def delete_task(self, task_id: str):
        success, message = self.task_service.delete_task(task_id)
        print(message)
    
    def change_task_status(self, task_id: str, status: str):
        success, message = self.task_service.change_task_status(task_id, status)
        print(message)
    
    def list_tasks(self, project_name: str = None):
        if project_name:
            success, result = self.task_service.list_tasks_by_project(project_name)
            if not success:
                print(result)
                return
            
            if not result:
                print("No tasks found for this project")
                return
            
            print(f"\n=== Tasks for Project: {project_name} ===")
            for task in result:
                self.display_task(task)
        else:
            tasks = self.task_service.list_all_tasks()
            if not tasks:
                print("No tasks found")
                return
            
            print("\n=== All Tasks ===")
            for task in tasks:
                self.display_task(task)
    
    def show_overdue_tasks(self):
        tasks = self.task_service.get_overdue_tasks()
        if not tasks:
            print("No overdue tasks found")
            return
        
        print("\n=== Overdue Tasks ===")
        for task in tasks:
            self.display_task(task)
    
    def close_overdue_tasks(self):
        success, message = self.task_service.close_overdue_tasks()
        print(message)
