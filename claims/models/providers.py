from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, CheckConstraint
from sqlalchemy.orm import Session
from claims.models.base_model import DBBaseModel


class Provider(DBBaseModel):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    npi = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "npi >= 1000000000 AND npi < 9999999999", name="npi_ten_digit_check"
        ),
    )