TodoList Application

A robust Python-based TodoList application built with SQLAlchemy ORM, following clean architecture principles with repository pattern and dependency injection.
Architecture & Design Patterns

    Clean Architecture with clear separation of concerns

    Repository Pattern for data access abstraction

    Dependency Injection for loose coupling

    Layered Architecture (Models → Repositories → Services → CLI)

    SQLAlchemy ORM for database operations

Database & Persistence

    PostgreSQL support with Docker containerization

    SQLite for development and testing

    SQLAlchemy 2.0 with declarative models

    Alembic for database migrations

    Proper relationships with cascade delete

Core Features

    Project Management (Create, Read, Update, Delete)

    Task Management with status tracking (todo/doing/done)

    Deadline support with overdue detection

    Auto-closing of overdue tasks - Scheduled Tasks Functionality

    Input validation and business rules enforcement

    Configurable limits via environment variables

Technical Stack

    Python 3.8+ with type hints

    Poetry for dependency management

    SQLAlchemy ORM with PostgreSQL/SQLite

    Click for CLI interface

    Schedule for background tasks

    Docker for database containerization

Project Structure

todolist/
├── app/
│   ├── exceptions/          # Custom exception classes
│   ├── models/              # SQLAlchemy ORM models
│   ├── repositories/        # Data access layer
│   ├── services/            # Business logic layer
│   ├── commands/            # CLI commands and scheduled tasks
│   ├── cli/                 # Command-line interface
│   └── db/                  # Database configuration
├── alembic/                 # Database migrations
├── tests/                   # Test suites
├── main.py                  # Application entry point
├── config.py               # Configuration management
├── docker-compose.yml      # PostgreSQL setup
├── pyproject.toml          # Poetry configuration
└── .env                    # Environment variables

Quick Start
Prerequisites

    Python 3.8+

    Poetry (recommended) or pip

    Docker (for PostgreSQL) - optional

Installation

    Clone and setup:

bash

# Install dependencies with Poetry
poetry install

# Or with pip
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

    Configure environment:

bash

cp .env.example .env
# Edit .env with your database settings

    Initialize database:

bash

# Create tables
python main.py init-db

Running the Application
Interactive CLI Mode
bash

python main.py interactive

Available commands in interactive mode:

    create_project "Name" "Description"

    list_projects

    edit_project "OldName" "NewName" "Description"

    delete_project "Name"

    create_task "ProjectName" "Title" "Description" [Deadline]

    list_tasks [ProjectName]

    edit_task "TaskID" "NewTitle" "Description" "Status"

    change_status "TaskID" "Status"

    delete_task "TaskID"

    show_overdue - Display all overdue tasks

    close_overdue - Manually close all overdue tasks

    exit

Individual Commands
bash

# One-time overdue task closure
python main.py autoclose

# Start background scheduler (runs every 15 minutes)
python main.py scheduler

# Initialize database
python main.py init-db

Scheduled Tasks Functionality

The application includes comprehensive scheduled tasks functionality for automatic management of overdue tasks:
Available Commands
Interactive Mode:

    show_overdue - Lists all tasks that have passed their deadline but are not marked as "done"

    close_overdue - Manually closes all overdue tasks (sets status to "done" and records closure timestamp)

Standalone Commands:

    python main.py autoclose - One-time execution to close all overdue tasks

    python main.py scheduler - Starts the background scheduler that automatically closes overdue tasks at configured intervals

How It Works

    Overdue Detection: Tasks are considered overdue when:

        deadline < current_time AND status != 'done'

    Auto-Closing: Overdue tasks are automatically:

        Marked as status = 'done'

        closed_at timestamp set to current time

    Scheduling: The background scheduler runs every 15 minutes by default (configurable)

Testing Scheduled Tasks
bash

# Create overdue tasks for testing
python main.py interactive --command 'create_task "Work" "Overdue Task" "Test overdue functionality" "2020-01-01"'

# Check overdue tasks
python main.py interactive --command 'show_overdue'

# Close overdue tasks manually
python main.py interactive --command 'close_overdue'

# Or use standalone command
python main.py autoclose

# Start automatic scheduler
python main.py scheduler

Configuration

Set the auto-close interval in .env:
env

AUTO_CLOSE_INTERVAL_MINUTES=15

Testing Your Application
Manual Testing Commands
bash

# Test project creation
python main.py interactive --command 'create_project "Work" "Work tasks"'

# Test task creation
python main.py interactive --command 'create_task "Work" "Finish report" "Quarterly report"'

# List all data
python main.py interactive --command 'list_projects'
python main.py interactive --command 'list_tasks'

# Test overdue functionality
python main.py interactive --command 'create_task "Work" "Overdue task" "Test" "2020-01-01"'
python main.py interactive --command 'show_overdue'
python main.py interactive --command 'close_overdue'

Automated Testing
bash

# Run the complete test suite
python test_app.py

# Run minimal database test
python simple_test.py

# Interactive testing
python interactive_test.py

Testing Error Handling
bash

# Test duplicate project
python main.py interactive --command 'create_project "Work" "Duplicate"'

# Test validation limits
python main.py interactive --command 'create_task "Work" "A" "Short"'

# Test non-existent project
python main.py interactive --command 'create_task "NonExistent" "Test" "Test"'

Database Management
Database Inspection
Option 1: DB Browser (GUI)
bash

# Install and open
sudo pacman -S sqlitebrowser
sqlitebrowser todolist.db

Option 2: SQLite CLI
bash

sqlite3 todolist.db

-- Useful commands:
.tables
.schema projects
SELECT * FROM projects;
SELECT * FROM tasks;
.quit

Option 3: Python Browser
bash

python db_browser.py

Option 4: Web Dashboard
bash

python web_dashboard.py
# Open http://localhost:5000

Database Configuration

The application supports both SQLite and PostgreSQL:

SQLite (Default):
env

DATABASE_URL=sqlite:///todolist.db

PostgreSQL:
env

DATABASE_URL=postgresql://user:pass@localhost:5432/todolist

To use PostgreSQL:
bash

# Start PostgreSQL with Docker
docker-compose up -d

# Update .env with PostgreSQL URL

Database Schema

Projects Table:

    id (UUID) - Primary key

    name (String) - Unique project name

    description (Text) - Project description

    created_at (DateTime) - Creation timestamp

Tasks Table:

    id (UUID) - Primary key

    project_id (UUID) - Foreign key to projects

    title (String) - Task title

    description (Text) - Task description

    status (Enum) - todo/doing/done

    deadline (DateTime) - Optional deadline

    created_at (DateTime) - Creation timestamp

    closed_at (DateTime) - Completion timestamp

Configuration
Environment Variables (.env)
env

# Database
DATABASE_URL=sqlite:///todolist.db

# Application Limits
MAX_NUMBER_OF_PROJECTS=10
MAX_NUMBER_OF_TASKS=50
MAX_PROJECT_NAME_LENGTH=30
MAX_PROJECT_DESCRIPTION_LENGTH=150
MAX_TASK_TITLE_LENGTH=30
MAX_TASK_DESCRIPTION_LENGTH=150

# Auto-close Settings
AUTO_CLOSE_INTERVAL_MINUTES=15

Business Rules

    Project names must be unique

    Task titles must be unique within a project

    Character limits enforced for all text fields

    Maximum project and task limits configurable

    Overdue tasks automatically closable

Troubleshooting
Common Issues

Database Connection Issues:
bash

# Reinitialize database
python main.py init-db

# Check database file
ls -la todolist.db

Import Errors:
bash

# Ensure virtual environment is activated
poetry shell
# or
source venv/bin/activate

# Verify installations
python -c "import sqlalchemy; print('SQLAlchemy OK')"

Poetry Issues:
bash

# Regenerate lock file
rm poetry.lock
poetry lock
poetry install --no-root

Debugging

Use the debug script to identify issues:
bash

python debug_app.py

Key Features Demonstrated

    Object-Relational Mapping - SQLAlchemy models with relationships

    Repository Pattern - Abstract data access layer

    Dependency Injection - Clean service initialization

    Business Logic Separation - Services contain domain logic

    Configuration Management - Environment-based settings

    Error Handling - Custom exceptions and validation

    Scheduled Tasks - Background job processing for auto-closing overdue tasks

    CLI Interface - User-friendly command-line interface

    Database Migrations - Alembic for schema changes

    Testing - Comprehensive test coverage

Next Steps
Potential Enhancements

    Web interface with FastAPI

    User authentication and authorization

    Task categories and tags

    Task priorities and sorting

    Data export/import functionality

    Email notifications for deadlines

    REST API endpoints

    Frontend React/Vue application

Production Deployment

    Environment-specific configurations

    Database connection pooling

    Logging and monitoring

    Containerization with Docker

    CI/CD pipeline setup

