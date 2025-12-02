# TodoList Application

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

<img width="1920" height="1080" alt="Screenshot From 2025-11-21 13-14-54" src="https://github.com/user-attachments/assets/b2be0ade-6cbd-47ca-9292-76720aee8ce6" />

<img width="1920" height="1080" alt="Screenshot From 2025-11-21 13-14-43" src="https://github.com/user-attachments/assets/67fac123-508a-476a-932f-4e5d7360f089" />


Phase 1: In-Memory OOP Implementation
Development Methodology

    Incremental Development: Breaking system into small, independent modules

    Agile Principles: Rapid feedback cycles and continuous delivery

    Definition of Done: Each phase delivers testable, usable functionality

Core Requirements
Functional Requirements

    Project Management: Create, edit, delete, list projects

    Task Management: Create, edit, delete tasks, status change (todo/doing/done)

    Constraints Enforcement: Character limits, duplicate prevention

    Configurable Limits: Environment-based configuration via .env

Non-Functional Requirements

    Code Readability: PEP8 compliance and coding conventions

    Maintainability: Clean OOP structure with layered architecture

    User Experience: Clear error messages and intuitive interface

    Extensibility: Preparation for future persistent storage

Key Concepts Implemented

    Object-Oriented Programming: Proper class design and encapsulation

    Separation of Concerns: Business logic separated from UI layer

    Configuration Management: Environment variables via .env

    Version Control: Git workflow with feature branches

    Dependency Management: Poetry for package management

Business Rules

    Project names must be unique

    Task titles must be unique within a project

    Character limits enforced (configurable via environment variables)

    Maximum project and task limits (configurable)

    Cascade delete: Deleting a project removes all its tasks

    Phase 2: Relational Database Migration
Database Implementation

    PostgreSQL: Primary production database

    SQLite: Development and testing database

    Docker Containerization: Isolated database environment

    SQLAlchemy 2.0: Modern ORM with declarative models

    Alembic: Database migration management

Database Schema Design
Tables Structure
sql

-- Projects Table
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    name VARCHAR(30) UNIQUE NOT NULL,
    description TEXT(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks Table
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(30) NOT NULL,
    description TEXT(150),
    status VARCHAR(10) CHECK (status IN ('todo', 'doing', 'done')),
    deadline TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP,
    UNIQUE(project_id, title)
);

Relationships

    One-to-Many: Project → Tasks (Cascade delete enabled)

    Primary Keys: UUID for unique identification

    Foreign Keys: Proper referential integrity

    Constraints: Unique constraints, check constraints, length limits

Architecture Patterns
Repository Pattern
text

┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Service   │─── │  Repository  │─── │  Database   │
│   Layer     │    │   Layer      │    │   Layer     │
└─────────────┘    └──────────────┘    └─────────────┘

Layered Architecture
text

Presentation Layer (CLI)
         ↓
Business Logic Layer (Services)
         ↓
Data Access Layer (Repositories)
         ↓
Database Layer (SQLAlchemy Models)

Scheduled Tasks Implementation

    Auto-closing Overdue Tasks: Automatic closure of tasks past deadline

    Two Implementation Options:

        System-level Cron Jobs: OS-level scheduling

        Python Schedule Library: Application-level scheduling

    Configurable Intervals: Auto-close interval configurable via environment variables

Key Technical Concepts

    ORM (Object-Relational Mapping): Bridge between Python objects and database tables

    Migrations: Version-controlled database schema changes

    Dependency Injection: Clean service initialization

    Transaction Management: ACID compliance

    Connection Pooling: Efficient database connections

Phase 3: Web API with FastAPI
API Design Philosophy

    RESTful Principles: Resource-based design with proper HTTP methods

    Stateless Architecture: Each request contains all necessary information

    Versioned API: /api/v1/ prefix for future compatibility

    Consistent Response Structure: Standardized success/error responses

    Comprehensive Documentation: Auto-generated OpenAPI/Swagger docs

API Endpoints
Projects Resource
text

GET    /api/v1/projects          # List all projects
POST   /api/v1/projects          # Create new project
GET    /api/v1/projects/{id}     # Get specific project
PUT    /api/v1/projects/{id}     # Replace entire project
PATCH  /api/v1/projects/{id}     # Partial project update
DELETE /api/v1/projects/{id}     # Delete project

Tasks Resource
text

GET    /api/v1/projects/{id}/tasks    # List tasks in project
POST   /api/v1/projects/{id}/tasks    # Create task in project
GET    /api/v1/tasks/{id}             # Get specific task
PUT    /api/v1/tasks/{id}             # Replace entire task
PATCH  /api/v1/tasks/{id}             # Partial task update
DELETE /api/v1/tasks/{id}             # Delete task
PATCH  /api/v1/tasks/{id}/status      # Update task status
POST   /api/v1/tasks/close-overdue    # Close all overdue tasks
GET    /api/v1/tasks/overdue          # List overdue tasks

HTTP Methods Usage
Method	Purpose	Idempotent	Safe
GET	Retrieve resource(s)	Yes	Yes
POST	Create new resource	No	No
PUT	Replace entire resource	Yes	No
PATCH	Partially update resource	No*	No
DELETE	Remove resource	Yes	No
Request/Response Components
Request Parts
python

# Headers - Metadata about request
{
    "Content-Type": "application/json",
    "Authorization": "Bearer <token>",
    "Accept": "application/json"
}

# Path Parameters - Required resource identifiers
/api/v1/projects/12345

# Query Parameters - Optional filters/pagination
/api/v1/tasks?status=doing&limit=10&page=2

# Body - Main request data (for POST/PUT/PATCH)
{
    "name": "Project Name",
    "description": "Project description"
}

Response Structure
json

// Success Response
{
    "status": "success",
    "data": { /* resource data */ },
    "message": "Operation successful"
}

// Error Response
{
    "status": "error",
    "message": "Project not found",
    "code": 404,
    "details": { /* validation errors */ }
}

Data Validation with Pydantic
Request Schema Example
python

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=30)
    description: str = Field(max_length=150)
    status: str = Field(default="todo", regex="^(todo|doing|done)$")
    deadline: Optional[datetime] = None
    
    @validator("deadline")
    def validate_deadline(cls, value):
        if value and value < datetime.now():
            raise ValueError("Deadline cannot be in the past")
        return value

Response Schema Example
python

class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    status: str
    deadline: Optional[datetime]
    created_at: datetime
    closed_at: Optional[datetime]
    
    class Config:
        from_attributes = True  # For ORM compatibility

Synchronous vs Asynchronous Operations
Sync Operations
python

@app.get("/projects/{project_id}")
def get_project(project_id: int):
    """Synchronous endpoint for CPU-bound operations"""
    project = project_service.get_project(project_id)
    return project

Async Operations
python

@app.get("/projects/{project_id}/tasks")
async def get_project_tasks(project_id: int):
    """Asynchronous endpoint for I/O-bound operations"""
    tasks = await task_service.get_tasks_by_project(project_id)
    return tasks

Automatic Documentation
Swagger UI Features

    Interactive API Explorer: Try endpoints directly from browser

    Request/Response Examples: Pre-filled examples for all endpoints

    Authentication Testing: Test protected endpoints with tokens

    Schema Documentation: Detailed data models with constraints

    Error Response Documentation: All possible error responses

Access Points

    Swagger UI: http://localhost:8000/docs

    ReDoc: http://localhost:8000/redoc

    OpenAPI JSON: http://localhost:8000/openapi.json

Security Considerations
HTTPS Implementation
python

# FastAPI HTTPS configuration
from fastapi import FastAPI
import ssl

app = FastAPI()

# SSL context for HTTPS
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(
    certfile="path/to/cert.pem",
    keyfile="path/to/key.pem"
)

# Run with HTTPS
uvicorn.run(app, host="0.0.0.0", port=8000, ssl=ssl_context)

Security Headers
python

from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Force HTTPS
app.add_middleware(HTTPSRedirectMiddleware)

# Trusted hosts
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com"])

🏗️ Complete Project Architecture
Multi-Layer Architecture Diagram
text

<img width="538" height="714" alt="Screenshot From 2025-12-02 18-26-56" src="https://github.com/user-attachments/assets/e11e1bce-7a3a-4c3c-b8b9-b4bb8114a62a" />


Project Structure (Phase 3 Final)
text

<img width="433" height="771" alt="Screenshot From 2025-12-02 18-25-10" src="https://github.com/user-attachments/assets/9e5a369b-1e40-4f96-97a7-9b960f93880e" />


🔧 Configuration Management
Environment Variables (.env)
env

# ===== Application Settings =====
APP_NAME="TodoList API"
APP_VERSION="1.0.0"
DEBUG=true
HOST=0.0.0.0
PORT=8000

# ===== Database Configuration =====
# Development (SQLite)
DATABASE_URL=sqlite:///todolist.db

# Production (PostgreSQL)
# DATABASE_URL=postgresql://user:password@localhost:5432/todolist

# ===== Application Limits =====
MAX_NUMBER_OF_PROJECTS=10
MAX_NUMBER_OF_TASKS=50
MAX_PROJECT_NAME_LENGTH=30
MAX_PROJECT_DESCRIPTION_LENGTH=150
MAX_TASK_TITLE_LENGTH=30
MAX_TASK_DESCRIPTION_LENGTH=150

# ===== Scheduled Tasks =====
AUTO_CLOSE_INTERVAL_MINUTES=15

# ===== API Security =====
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
API_KEY=your_secret_api_key_here
JWT_SECRET=your_jwt_secret_key_here
