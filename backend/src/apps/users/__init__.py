try:
    from src.settings.database import Base
except Exception as e:
    from settings.database import Base

Base = Base