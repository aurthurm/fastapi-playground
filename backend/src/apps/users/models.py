from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

try:
    from apps.users import Base
except ModuleNotFoundError as e: #ImportError
     # for alembic to work properly >> one dir up
    from src.apps.users import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
