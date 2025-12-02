from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class ProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Project name")
    description: Optional[str] = Field(None, description="Project description")

class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime] = None  # Make sure this is Optional with default None
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
