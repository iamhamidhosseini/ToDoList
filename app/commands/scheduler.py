import schedule
import time
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from config import Config

def run_scheduler():
    print("Starting task scheduler...")
    
    # Set up the scheduled task
    interval_minutes = Config.AUTO_CLOSE_INTERVAL_MINUTES
    schedule.every(interval_minutes).minutes.do(run_autoclose)
    
    print(f"Auto-close scheduled to run every {interval_minutes} minutes")
    print("Press Ctrl+C to stop the scheduler")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nScheduler stopped")

def run_autoclose():
    try:
        task_repository = TaskRepository()
        project_repository = ProjectRepository()
        task_service = TaskService(task_repository, project_repository)
        
        success, message = task_service.close_overdue_tasks()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}")
        
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error: {e}")

if __name__ == "__main__":
    run_scheduler()
