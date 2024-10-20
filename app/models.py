import uuid
from datetime import date
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class AnnouncementBase(SQLModel):
    code: str = Field(max_length=60)
    abbr: str = Field(max_length=100)
    title: str = Field(max_length=200)
    url: str = Field(max_length=200, unique=True)
    publish_date: date = Field(default=None)
    source_key: str = Field(max_length=100)
    source: str = Field(max_length=100)
    type: str = Field(max_length=30)


class Announcement(AnnouncementBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class AnnouncementCreate(AnnouncementBase):
    pass


class AnnouncementFilter(BaseModel):
    date_start: str
    date_end: str
    types: list[str] | None = None
    search: str | None = None
    page: int = 1
    page_size: int = 20


class AnnouncementPage(SQLModel):
    total: int
    items: list[Announcement]
