from fastapi import APIRouter
from apps import login
from apps.users import routes as user_routes


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(user_routes.router, prefix="/users", tags=["users"])
