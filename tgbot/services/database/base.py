from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy import Column, TIMESTAMP, func


Base = declarative_base()


class TimedBaseModel(Base):
    __abstract__ = True

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())