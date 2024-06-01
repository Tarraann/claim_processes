from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from claims.models.base_model import DBBaseModel


class Subscriber(DBBaseModel):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subscriber_number = Column(Integer, nullable=False)

