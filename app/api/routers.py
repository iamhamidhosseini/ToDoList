from fastapi import APIRouter
from app.api.controllers import projects_controller, tasks_controller

api_router = APIRouter()

api_router.include_router(projects_controller.router)
api_router.include_router(tasks_controller.router)
