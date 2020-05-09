from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

try:
    from settings import config
except ModuleNotFoundError as e: #ImportError
     # for alembic to work properly >> one dir up
    from src.settings import config


engine = create_engine(config.SQLALCHEMY_DATABASE_URI) # connect_args={'check_same_thread': False}) #pool_pre_ping=True, connect_args are only for sqlite
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class CustomBase(object):
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()