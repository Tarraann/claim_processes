from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import Session
from claims.models.base_model import DBBaseModel


class Claim(DBBaseModel):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_date = Column(DateTime, nullable=False)
    quadrant = Column(String, nullable=True)
    provider_id = Column(Integer, nullable=False)
    procedure_id = Column(Integer, nullable=False)
    plan_id = Column(Integer, nullable=False)
    subscriber_id = Column(Integer, nullable=False)
    provider_fees = Column(Float, nullable=False, default=0)
    allowed_fees = Column(Float, null=False, default=0)
    member_coinsurance = Column(Float, nullable=False, default=0)
    member_copay = Column(Float, nullable=False, default=0)
    net_fee = Column(Float, nullable=False, default=0)
