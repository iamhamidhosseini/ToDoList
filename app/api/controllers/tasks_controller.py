from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.api.controller_schemas.requests.task_request import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskResponse
)
from app.db.session import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreateRequest, db: Session = Depends(get_db)):
    
    from app.models.task import Task
    from app.models.project import Project
    
    try:
        # Find project by name
        project = db.query(Project).filter(Project.name == task.project_name).first()
        if not project:
            raise HTTPException(status_code=404, detail=f"Project '{task.project_name}' not found")
        
        # Create new task
        db_task = Task(
            id=str(uuid.uuid4()),
            project_id=project.id,
            title=task.title,
            description=task.description,
            status=task.status,
            deadline=datetime.fromisoformat(task.deadline) if task.deadline else None
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    project_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    
    from app.models.task import Task
    query = db.query(Task)
    if project_id:
        query = query.filter(Task.project_id == project_id)
    tasks = query.order_by(Task.created_at).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    
    from app.models.task import Task
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str, 
    task_data: TaskUpdateRequest, 
    db: Session = Depends(get_db)
):
    
    from app.models.task import Task
    
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        update_data = task_data.dict(exclude_unset=True)
        
        # Convert deadline string to datetime if provided
        if 'deadline' in update_data and update_data['deadline']:
            try:
                update_data['deadline'] = datetime.fromisoformat(update_data['deadline'])
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid deadline format. Use YYYY-MM-DD")
        
        for field, value in update_data.items():
            setattr(task, field, value)
        z
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    
    from app.models.task import Task
    
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        db.delete(task)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/overdue/", response_model=List[TaskResponse])
def get_overdue_tasks(db: Session = Depends(get_db)):
    
    from app.models.task import Task, TaskStatus
    from datetime import datetime
    now = datetime.utcnow()
    tasks = db.query(Task).filter(
        Task.deadline < now,
        Task.status != TaskStatus.DONE
    ).all()
    return tasks

@router.post("/overdue/close/", status_code=status.HTTP_200_OK)
def close_overdue_tasks(db: Session = Depends(get_db)):
    
    from app.models.task import Task, TaskStatus
    from datetime import datetime
    
    try:
        now = datetime.utcnow()
        
        overdue_tasks = db.query(Task).filter(
            Task.deadline < now,
            Task.status != TaskStatus.DONE
        ).all()
        
        for task in overdue_tasks:
            task.status = TaskStatus.DONE
            task.closed_at = now
        
        db.commit()
        return {"message": f"Closed {len(overdue_tasks)} overdue task(s)"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
