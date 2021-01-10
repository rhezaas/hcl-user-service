from sqlalchemy import Column, String, Integer, Text, DateTime
from database import Database
from sqlalchemy.orm import relationship
import datetime


class User(Database.Base):
    __tablename__ = 'user'
    __table_args__ = {
        'schema': 'user',
        'extend_existing': True
    }

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, default=datetime.datetime.now)

    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # noqa: E501

    firstname = Column(String(length=100), nullable=False)

    lastname = Column(String(length=100), nullable=False)

    profile = Column(Text)

    phone = Column(String(50), nullable=False)

    deleted_at = Column(DateTime)

    account = relationship('Account', uselist=False, back_populates='user')

    images = relationship('Image', back_populates='user')

    def __init__(
        self,
        firstname: str,
        lastname: str,
        phone: str,
        profile: str = None,
        deleted_at: str = None
    ):
        self.firstname = firstname
        self.lastname = lastname
        self.profile = profile
        self.phone = phone
        self.deleted_at = deleted_at
