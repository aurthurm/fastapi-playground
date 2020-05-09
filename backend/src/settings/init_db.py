from apps.users import crud
from settings import config
from apps.users.schemas import UserCreate
from settings.database import engine

import logging, coloredlogs
coloredlogs.install()
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize properly relationships
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from settings.database import Base


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db_session, email=config.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = UserCreate(
            email=config.FIRST_SUPERUSER_EMAIL,
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db_session, obj_in=user_in)
    else:
        logger.error(f" A super user with email {config.FIRST_SUPERUSER_EMAIL} already exists.")
