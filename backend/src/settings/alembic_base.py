# Import all the models, so that Base has them before being
# imported by Alembic

from src.settings.database import Base  #noqa
from src.apps.users.models import User  #noqa
from src.apps.shop.product.models import *

