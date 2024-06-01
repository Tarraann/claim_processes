from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from claims.models.base_model import DBBaseModel


class Plan(DBBaseModel):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    plan_group = Column(String, nullable=False)

