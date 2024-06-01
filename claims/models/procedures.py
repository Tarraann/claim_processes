from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, CheckConstraint
from sqlalchemy.orm import Session
from claims.models.base_model import DBBaseModel


class Procedure(DBBaseModel):
    __tablename__ = "procedures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint(
            CheckConstraint("code LIKE 'D%'", name="code_starts_with_d")
        ),
    )