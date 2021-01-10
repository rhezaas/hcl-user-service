from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey  # noqa: E501
from database import Database
from sqlalchemy.orm import relationship
import datetime


class Image(Database.Base):
    __tablename__ = 'image'
    __table_args__ = {
        'schema': 'user',
        'extend_existing': True
    }

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, default=datetime.datetime.now)

    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)  # noqa: E501

    image = Column(Text, nullable=False)

    width = Column(Integer)

    height = Column(Integer)

    deleted_at = Column(DateTime)

    user_id = Column(Integer, ForeignKey('user.user.id'), nullable=False)  # noqa: E501

    user = relationship('User', uselist=False, back_populates='images')

    def __init__(self, image: str, width: str, height: str, deleted_at: str):  # noqa: E501
        self.image = image
        self.width = width
        self.height = height
        self.deleted_at = deleted_at
