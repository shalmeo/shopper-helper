from sqlalchemy import BigInteger, Column, String

from tgbot.services.database.base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'User'
    
    id = Column(BigInteger, primary_key=True)
    full_name = Column(String, nullable=False)