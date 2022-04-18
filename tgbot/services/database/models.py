import sqlalchemy as sa

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from tgbot.services.database.base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'user'
    
    id = sa.Column(sa.BigInteger, primary_key=True, unique=True)
    full_name = sa.Column(sa.String, nullable=False)
    premium = sa.Column(sa.Boolean, default=False)
    
    tracks = relationship('Track', backref='user', uselist=True)
    

class Track(TimedBaseModel):
    __tablename__ = 'track'
    
    id = sa.Column(UUID, primary_key=True, unique=True)
    brand = sa.Column(sa.String)
    name = sa.Column(sa.String)
    price = sa.Column(sa.Integer)
    vendore_code = sa.Column(sa.String)
    size_name = sa.Column(sa.String)
    option_id = sa.Column(sa.BigInteger)
    stocks = sa.Column(sa.Boolean)
    threshold = sa.Column(sa.Integer, default=None)
    shop = sa.Column(sa.String)

    user_id = sa.Column(sa.BigInteger, sa.ForeignKey('user.id'))

    
class Shop(TimedBaseModel):
    __tablename__ = 'shop'
    
    id = sa.Column(sa.String, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    active = sa.Column(sa.Boolean, default=True)
