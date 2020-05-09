import logging, coloredlogs

from settings.init_db import init_db
from settings.database import db_session


coloredlogs.install()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init():
    init_db(db_session)


def main():
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
