import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

try:
    from apps.users import Base
except ModuleNotFoundError as e: #ImportError
     # for alembic to work properly >> one dir up
    from src.apps.users import Base


class SeoModel(Base):
    __abstract__ = True
    seo_title = Column(String(100))
    seo_description = Column(String(100))


class PublishableModel(Base):
    __abstract__ = True
    publication_date = Column(DateTime)
    is_published = Column(Boolean(), default=False)

    @property
    def is_visible(self):
        return self.is_published and (
            self.publication_date is None
            or self.publication_date < datetime.date.today()
        )
