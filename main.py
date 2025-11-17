from cli.commands import CLICommands
from storage.memory import MemoryStorage
from core.services import ProjectService, TaskService

class Application:
    def __init__(self):
        self.storage = MemoryStorage()
        self.project_service = ProjectService(self.storage)
        self.task_service = TaskService(self.storage, self.project_service)
        self.cli = CLICommands(self.project_service, self.task_service)
    
    def run(self):
        self._show_welcome_message()
        self._main_loop()
    
    def _show_welcome_message(self):
        print("=== ToDoList CLI ===")
        print("Available commands:")
        print("1. create_project <name> <description>")
        print("2. edit_project <project_name> <new_name> <new_description>")
        print("3. delete_project <project_name>")
        print("4. list_projects")
        print("5. create_task <project_name> <title> <description> [deadline]")
        print("6. edit_task <project_name> <task_title> <new_title> <description> <status>")
        print("7. delete_task <project_name> <task_title>")
        print("8. change_status <project_name> <task_title> <status>")
        print("9. list_tasks [project_name]")
        print("10. exit")
        print("\nStatus values: todo, doing, done")
        print("Deadline format: YYYY-MM-DD")
        print("You can use quotes for names/descriptions with spaces")
        print('Example: create_task work "Finish report" "Complete the quarterly report" 2024-01-15')
    
    def _main_loop(self):
        while True:
            try:
                user_input = input("\nEnter command: ").strip()
                
                if user_input.lower() == 'exit':
                    print("Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                parts = self._parse_input(user_input)
                command = parts[0]
                
                self._handle_command(command, parts)
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def _parse_input(self, user_input):
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
    
    def _handle_command(self, command: str, parts: list):
        if command == "create_project" and len(parts) >= 3:
            name = parts[1]
            description = parts[2] if len(parts) > 2 else ""
            self.cli.create_project(name, description)
        
        elif command == "edit_project" and len(parts) >= 4:
            project_name = parts[1]
            new_name = parts[2]
            description = parts[3] if len(parts) > 3 else ""
            self.cli.edit_project(project_name, new_name, description)
        
        elif command == "delete_project" and len(parts) == 2:
            project_name = parts[1]
            self.cli.delete_project(project_name)
        
        elif command == "list_projects":
            self.cli.list_projects()
        
        elif command == "create_task" and len(parts) >= 4:
            project_name = parts[1]
            title = parts[2]
            description = parts[3] if len(parts) > 3 else ""
            deadline = parts[4] if len(parts) > 4 else None
            self.cli.create_task(project_name, title, description, deadline)
        
        elif command == "edit_task" and len(parts) >= 6:
            project_name = parts[1]
            task_title = parts[2]
            new_title = parts[3]
            description = parts[4] if len(parts) > 4 else ""
            status = parts[5] if len(parts) > 5 else "todo"
            self.cli.edit_task(project_name, task_title, new_title, description, status)
        
        elif command == "delete_task" and len(parts) == 3:
            project_name = parts[1]
            task_title = parts[2]
            self.cli.delete_task(project_name, task_title)
        
        elif command == "change_status" and len(parts) == 4:
            project_name = parts[1]
            task_title = parts[2]
            status = parts[3]
            self.cli.change_task_status(project_name, task_title, status)
        
        elif command == "list_tasks":
            project_name = parts[1] if len(parts) > 1 else None
            self.cli.list_tasks(project_name)
        
        else:
            print("Invalid command or missing parameters")
            print("Use 'exit' to quit or check the command format above")

def main():
    app = Application()
    app.run()

if __name__ == "__main__":
    main()
