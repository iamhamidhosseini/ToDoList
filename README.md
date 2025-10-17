
# ToDoList - Python OOP Project

A simple yet powerful task management system built with Python using Object-Oriented Programming principles. This project demonstrates clean architecture, modular design, and follows Python best practices.

## Features

- Project Management: Create, edit, and delete projects
- Task Management: Add, modify, and remove tasks within projects
- Status Tracking: Track task progress with todo/doing/done statuses
- In-Memory Storage: Fast, temporary data storage (resets on program close)
- CLI Interface: Simple command-line interface for all operations
- Configuration Management: Environment-based configuration using `.env` files
- Input Validation: Comprehensive validation for names and descriptions
- Cascade Delete: Automatic task deletion when projects are removed

## Installation

### Prerequisites
- Python 3.8 or higher
- Poetry (dependency management)

### Usage
Available Commands

### Project Management:

    create_project <name> <description> - Create a new project

    edit_project <project_name> <new_name> <new_description> - Edit project details

    delete_project <project_name> - Delete a project and all its tasks

    list_projects - Display all projects

### Task Management:

    create_task <project_name> <title> <description> - Add a task to a project

    edit_task <project_name> <task_title> <new_title> <description> <status> - Modify task details

    delete_task <project_name> <task_title> - Remove a task from a project

    list_tasks <project_name> - View all tasks in a project

### System:

    exit - Quit the application

## Status Values

### Tasks can have one of three statuses:

    todo - Task is pending

    doing - Task is in progress

    done - Task is completed

# Example 

  ```
  # Create projects
  create_project work "Work related tasks"
  create_project personal "Personal tasks"
  
  # Add tasks
  create_task work "Finish report" "Complete the quarterly report"
  create_task personal "Buy
  ```



