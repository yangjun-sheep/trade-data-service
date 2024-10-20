from fastapi import APIRouter

from app.api.deps import SessionDep
from app.models import AnnouncementPage, AnnouncementFilter
from app.crud import CRUDAnnouncement
router = APIRouter()


@router.get("", response_model=AnnouncementPage)
def query_announcements(
    session: SessionDep,
    date_start: str,
    date_end: str,
    types: str | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 20
) -> AnnouncementPage:
    """
    Retrieve items.
    """
    announcement_crud = CRUDAnnouncement(session)
    filter = AnnouncementFilter(
        date_start=date_start,
        date_end=date_end,
        search=search,
        page=page,
        page_size=page_size
    )
    if types:
        filter.types = types.split(',')
    return announcement_crud.page(filter)


@router.get("/types", response_model=list[str])
def query_announcement_types(session: SessionDep) -> list[str]:
    """
    Retrieve items.
    """
    announcement_crud = CRUDAnnouncement(session)
    return announcement_crud.get_types()
