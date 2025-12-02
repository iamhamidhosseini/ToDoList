#!/usr/bin/env python3
import sys

def run_api():
    from fastapi import FastAPI
    import uvicorn
    
    app = FastAPI(
        title="ToDoList API",
        version="1.0.0",
        description="API for managing ToDoList projects and tasks",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Import routers here to avoid circular imports at module level
    from app.api.routers import api_router
    app.include_router(api_router, prefix="/api/v1")
    
    @app.get("/")
    def root():
        return {
            "message": "Welcome to ToDoList API",
            "docs": "/docs",
            "redoc": "/redoc",
            "note": "CLI is deprecated. Use API endpoints instead."
        }
    
    @app.get("/health")
    def health_check():
        return {"status": "healthy"}
    
    print("=" * 60)
    print("Starting ToDoList API server...")
    print("API Documentation: http://localhost:8001/docs")
    print("CLI is deprecated. Please use the API instead.")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)

def run_cli():
    """Run CLI (deprecated)"""
    import click
    from app.cli.console import CLICommands
    from app.services.project_service import ProjectService
    from app.services.task_service import TaskService
    from app.repositories.project_repository import ProjectRepository
    from app.repositories.task_repository import TaskRepository
    from app.db.session import db_session
    from app.commands.autoclose_overdue import autoclose_overdue
    from app.commands.scheduler import run_scheduler
    
    @click.group()
    def cli():
        """Deprecated CLI interface for ToDoList"""
        print("=" * 60)
        print("WARNING: CLI interface is deprecated and will be removed in the next release.")
        print("Please use the FastAPI HTTP interface instead.")
        print("=" * 60)
    
    @cli.command()
    def interactive():
        # Initialize services with dependency injection
        project_repository = ProjectRepository()
        task_repository = TaskRepository()
        project_service = ProjectService(project_repository)
        task_service = TaskService(task_repository, project_repository)
        cli_commands = CLICommands(project_service, task_service)
        
        run_interactive_mode(cli_commands)
    
    @cli.command()
    def autoclose():
        """Auto close overdue tasks (deprecated)"""
        autoclose_overdue()
    
    @cli.command()
    def scheduler():
        run_scheduler()
    
    @cli.command()
    def init_db():
        """Initialize database (deprecated)"""
        try:
            db_session.create_tables()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    
    def run_interactive_mode(cli_commands: CLICommands):
        print("=== TodoList CLI (DEPRECATED) ===")
        print("Available commands:")
        print("1. create_project <name> <description>")
        print("2. edit_project <project_name> <new_name> <new_description>")
        print("3. delete_project <project_name>")
        print("4. list_projects")
        print("5. create_task <project_name> <title> <description> [deadline]")
        print("6. edit_task <task_id> <new_title> <description> <status>")
        print("7. delete_task <task_id>")
        print("8. change_status <task_id> <status>")
        print("9. list_tasks [project_name]")
        print("10. show_overdue")
        print("11. close_overdue")
        print("12. exit")
        print("\nStatus values: todo, doing, done")
        print("Deadline format: YYYY-MM-DD")
        
        while True:
            try:
                user_input = input("\nEnter command: ").strip()
                
                if user_input.lower() == 'exit':
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                parts = parse_input(user_input)
                command = parts[0]
                
                handle_command(command, parts, cli_commands)
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def parse_input(user_input):
        parts = []
        current_part = []
        in_quotes = False
        
        for char in user_input:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ' ' and not in_quotes:
                if current_part:
                    parts.append(''.join(current_part))
                    current_part = []
            else:
                current_part.append(char)
        
        if current_part:
            parts.append(''.join(current_part))
        
        return parts
    
    def handle_command(command: str, parts: list, cli_commands: CLICommands):
        if command == "create_project" and len(parts) >= 3:
            name = parts[1]
            description = parts[2] if len(parts) > 2 else ""
            cli_commands.create_project(name, description)
        
        elif command == "edit_project" and len(parts) >= 4:
            project_name = parts[1]
            new_name = parts[2]
            description = parts[3] if len(parts) > 3 else ""
            cli_commands.edit_project(project_name, new_name, description)
        
        elif command == "delete_project" and len(parts) == 2:
            project_name = parts[1]
            cli_commands.delete_project(project_name)
        
        elif command == "list_projects":
            cli_commands.list_projects()
        
        elif command == "create_task" and len(parts) >= 4:
            project_name = parts[1]
            title = parts[2]
            description = parts[3] if len(parts) > 3 else ""
            deadline = parts[4] if len(parts) > 4 else None
            cli_commands.create_task(project_name, title, description, deadline)
        
        elif command == "edit_task" and len(parts) >= 5:
            task_id = parts[1]
            title = parts[2]
            description = parts[3] if len(parts) > 3 else ""
            status = parts[4] if len(parts) > 4 else "todo"
            cli_commands.edit_task(task_id, title, description, status)
        
        elif command == "delete_task" and len(parts) == 2:
            task_id = parts[1]
            cli_commands.delete_task(task_id)
        
        elif command == "change_status" and len(parts) == 3:
            task_id = parts[1]
            status = parts[2]
            cli_commands.change_task_status(task_id, status)
        
        elif command == "list_tasks":
            project_name = parts[1] if len(parts) > 1 else None
            cli_commands.list_tasks(project_name)
        
        elif command == "show_overdue":
            cli_commands.show_overdue_tasks()
        
        elif command == "close_overdue":
            cli_commands.close_overdue_tasks()
        
        else:
            print("Invalid command or missing parameters")
            print("Use quotes for names/descriptions with spaces")
    
    # Remove 'cli' from sys.argv and run click CLI
    sys.argv = [sys.argv[0]] + sys.argv[2:]
    cli()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        run_cli()
    else:
        run_api()
