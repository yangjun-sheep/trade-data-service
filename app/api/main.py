from fastapi import APIRouter

from app.api.routes import announcements

api_router = APIRouter()
api_router.include_router(announcements.router, prefix="/announcements", tags=["announcements"])
