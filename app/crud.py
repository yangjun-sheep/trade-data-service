from typing import Any, Dict, Generic, Optional, Type, TypeVar
from datetime import date

from sqlmodel import SQLModel, select, Session, func, or_

from app.models import Announcement, AnnouncementCreate, AnnouncementPage, AnnouncementFilter


ModelType = TypeVar("ModelType", bound=SQLModel)


class CRUDBase(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, session: Session, model: Type[ModelType] = None):
        self.session = session
        self.model = model or self.model
        assert self.model is not None, "model is required"

    def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_by_filters(self, filters: Dict[str, Any]) -> Optional[ModelType]:
        return self.session.scalar(select(self.model).filter_by(**filters))


class CRUDAnnouncement(CRUDBase[Announcement]):
    def __init__(self, session: Session):
        super().__init__(session, Announcement)

    def create(self, announcement_create: AnnouncementCreate) -> Announcement:
        db_obj = Announcement.model_validate(announcement_create)
        super().create(db_obj)
        return db_obj

    def page(self, filter: AnnouncementFilter) -> AnnouncementPage:
        base_query = select(Announcement).where(
            Announcement.publish_date >= filter.date_start,
            Announcement.publish_date <= filter.date_end,
        )
        if filter.types:
            base_query = base_query.where(
                Announcement.type.in_(filter.types)
            )
        if filter.search:
            base_query = base_query.where(
                or_(
                    Announcement.title.like(f'%{filter.search}%'),
                    Announcement.abbr.like(f'%{filter.search}%'),
                    Announcement.code.like(f'%{filter.search}%')
                )
            )
        total = self.session.exec(select(func.count()).select_from(base_query)).one()
        item_query = base_query.offset((filter.page - 1) * filter.page_size).limit(filter.page_size)
        items = self.session.exec(item_query).all()
        return AnnouncementPage(total=total, items=items)

    def get_unique_keys(self, day: date, source: str) -> list[str]:
        filters = {
            'publish_date': day,
            'source': source
        }
        query = self.session.exec(select(func.distinct(Announcement.source_key)).filter_by(**filters))
        return query.all()

    def get_types(self) -> list[str]:
        query = self.session.exec(select(func.distinct(Announcement.type)))
        return query.all()
