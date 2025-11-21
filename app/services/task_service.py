from typing import List, Tuple, Optional
from datetime import datetime
from app.models.task import Task, TaskStatus
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.exceptions.service_exceptions import ValidationException, BusinessRuleException
from app.exceptions.repository_exceptions import TaskNotFoundException, ProjectNotFoundException, DuplicateTaskException
from config import Config

class TaskService:
    def __init__(self, task_repository: TaskRepository, project_repository: ProjectRepository):
        self.task_repository = task_repository
        self.project_repository = project_repository
    
    def create_task(self, project_name: str, title: str, description: str = "", deadline: Optional[datetime] = None) -> Tuple[bool, str]:
        try:
            # Get project
            project = self.project_repository.get_by_name(project_name)
            if not project:
                raise ProjectNotFoundException("Project not found")
            
            # Validation
            if not title.strip():
                raise ValidationException("Task title cannot be empty")
            
            if len(title) > Config.MAX_TASK_TITLE_LENGTH:
                raise ValidationException(f"Task title cannot exceed {Config.MAX_TASK_TITLE_LENGTH} characters")
            
            if len(description) > Config.MAX_TASK_DESCRIPTION_LENGTH:
                raise ValidationException(f"Task description cannot exceed {Config.MAX_TASK_DESCRIPTION_LENGTH} characters")
            
            if self.task_repository.count_by_project(project.id) >= Config.MAX_NUMBER_OF_TASKS:
                raise BusinessRuleException(f"Cannot exceed maximum number of tasks per project: {Config.MAX_NUMBER_OF_TASKS}")
            
            # Create task
            task = Task(
                project_id=project.id,
                title=title,
                description=description,
                deadline=deadline
            )
            created_task = self.task_repository.create(task)
            
            return True, f"Task '{created_task.title}' created successfully in project '{project.name}'"
        
        except (ValidationException, BusinessRuleException, ProjectNotFoundException, DuplicateTaskException) as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def edit_task(self, task_id: str, title: str, description: str = "", status: str = TaskStatus.TODO) -> Tuple[bool, str]:
        try:
            task = self.task_repository.get_by_id(task_id)
            if not task:
                raise TaskNotFoundException("Task not found")
            
            # Validation
            if not title.strip():
                raise ValidationException("Task title cannot be empty")
            
            if len(title) > Config.MAX_TASK_TITLE_LENGTH:
                raise ValidationException(f"Task title cannot exceed {Config.MAX_TASK_TITLE_LENGTH} characters")
            
            if len(description) > Config.MAX_TASK_DESCRIPTION_LENGTH:
                raise ValidationException(f"Task description cannot exceed {Config.MAX_TASK_DESCRIPTION_LENGTH} characters")
            
            # Validate status
            valid_statuses = [TaskStatus.TODO, TaskStatus.DOING, TaskStatus.DONE]
            if status not in valid_statuses:
                raise ValidationException(f"Status must be one of: {', '.join(valid_statuses)}")
            
            # Update task
            task.title = title
            task.description = description
            task.status = status
            
            # If marking as done, set closed_at
            if status == TaskStatus.DONE and not task.closed_at:
                task.closed_at = datetime.utcnow()
            
            updated_task = self.task_repository.update(task)
            
            return True, f"Task '{updated_task.title}' updated successfully"
        
        except (ValidationException, BusinessRuleException, TaskNotFoundException) as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def delete_task(self, task_id: str) -> Tuple[bool, str]:
        try:
            success = self.task_repository.delete(task_id)
            return True, "Task deleted successfully"
        
        except TaskNotFoundException as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def change_task_status(self, task_id: str, status: str) -> Tuple[bool, str]:
        try:
            task = self.task_repository.get_by_id(task_id)
            if not task:
                raise TaskNotFoundException("Task not found")
            
            # Validate status
            valid_statuses = [TaskStatus.TODO, TaskStatus.DOING, TaskStatus.DONE]
            if status not in valid_statuses:
                raise ValidationException(f"Status must be one of: {', '.join(valid_statuses)}")
            
            # Update status
            task.status = status
            
            # If marking as done, set closed_at
            if status == TaskStatus.DONE and not task.closed_at:
                task.closed_at = datetime.utcnow()
            
            self.task_repository.update(task)
            
            return True, f"Task status changed to '{status}'"
        
        except (ValidationException, BusinessRuleException, TaskNotFoundException) as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def list_tasks_by_project(self, project_name: str) -> Tuple[bool, str | List[Task]]:
        try:
            project = self.project_repository.get_by_name(project_name)
            if not project:
                raise ProjectNotFoundException("Project not found")
            
            tasks = self.task_repository.get_by_project_id(project.id)
            return True, tasks
        
        except ProjectNotFoundException as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
    
    def list_all_tasks(self) -> List[Task]:
        return self.task_repository.get_all()
    
    def get_overdue_tasks(self) -> List[Task]:
        return self.task_repository.get_overdue_tasks()
    
    def close_overdue_tasks(self) -> Tuple[bool, str]:
        try:
            closed_count = self.task_repository.close_overdue_tasks()
            return True, f"Closed {closed_count} overdue tasks"
        
        except Exception as e:
            return False, f"Error closing overdue tasks: {str(e)}"
