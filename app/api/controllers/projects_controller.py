from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.api.controller_schemas.requests.project_request import (
    ProjectCreateRequest, 
    ProjectUpdateRequest, 
    ProjectResponse
)
from app.db.session import get_db

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreateRequest, db: Session = Depends(get_db)):
    
    try:
        from app.models.project import Project
        
        # Check if project with same name exists
        existing = db.query(Project).filter(Project.name == project.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Project with this name already exists")
        
        # Create new project
        db_project = Project(
            id=str(uuid.uuid4()),
            name=project.name,
            description=project.description
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        # Convert SQLAlchemy object to dict with required fields
        return {
            "id": db_project.id,
            "name": db_project.name,
            "description": db_project.description,
            "created_at": db_project.created_at,
            "updated_at": None  # Explicitly set to None
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    
    from app.models.project import Project
    projects = db.query(Project).order_by(Project.created_at).all()
    
    # Convert each project to dict with updated_at field
    return [
        {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at,
            "updated_at": None
        }
        for project in projects
    ]

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str, db: Session = Depends(get_db)):
    
    from app.models.project import Project
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "created_at": project.created_at,
        "updated_at": None
    }

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: str, 
    project_data: ProjectUpdateRequest, 
    db: Session = Depends(get_db)
):
    
    from app.models.project import Project
    
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        update_data = project_data.dict(exclude_unset=True)
        
        # Check if new name conflicts with existing project
        if 'name' in update_data and update_data['name'] != project.name:
            existing = db.query(Project).filter(
                Project.name == update_data['name'],
                Project.id != project_id
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="Another project with this name already exists")
        
        for field, value in update_data.items():
            setattr(project, field, value)
        
        db.commit()
        db.refresh(project)
        
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at,
            "updated_at": None
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    
    from app.models.project import Project
    
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        db.delete(project)
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
