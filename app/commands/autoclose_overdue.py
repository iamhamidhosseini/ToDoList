import click
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository

@click.command()
def autoclose_overdue():
    click.echo("Starting auto-close of overdue tasks...")
    
    try:
        task_repository = TaskRepository()
        project_repository = ProjectRepository()
        task_service = TaskService(task_repository, project_repository)
        
        success, message = task_service.close_overdue_tasks()
        click.echo(message)
        
    except Exception as e:
        click.echo(f"Error: {e}")

if __name__ == "__main__":
    autoclose_overdue()
