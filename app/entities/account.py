from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
import datetime
from database import Database
from sqlalchemy.orm import relationship


class Account(Database.Base):
    __tablename__ = 'account'
    __table_args__ = {
        'schema': 'user',
        'extend_existing': True
    }

    id = Column(Integer, primary_key=True)

    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # noqa: E501

    username = Column(String(length=100), nullable=False)

    password = Column(String(length=100), nullable=False)

    token = Column(String(length=100))

    user_id = Column(Integer, ForeignKey('user.user.id'), unique=True, nullable=False)  # noqa: E501

    user = relationship('User', back_populates='account')

    def __init__(
        self,
        username: str,
        password: str,
        user_id: int,
        token: str = 'null'
    ):
        self.username = username
        self.password = password
        self.user_id = user_id
        self.token = token
