from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskCreateRequest(BaseModel):
    project_name: str = Field(..., description="Name of the project")
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    deadline: Optional[str] = Field(None, description="Format: YYYY-MM-DD")
    status: str = Field(default="todo", pattern="^(todo|doing|done)$")

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(todo|doing|done)$")
    deadline: Optional[str] = Field(None, description="Format: YYYY-MM-DD")

class TaskResponse(BaseModel):
    id: str  # Changed to str for UUID
    project_id: str  # Changed to str for UUID
    title: str
    description: Optional[str]
    status: str
    deadline: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
