from datetime import datetime

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

    @classmethod
    def create_claim(cls, session: Session, service_date: datetime, quadrant: str, provider_id: int, procedure_id: int,
                     plan_id: int, subscriber_id: int, provider_fees: float, allowed_fees: float, member_coinsurance: float,
                     member_copay: float, net_fee: float):
        claim = Claim(
            service_date=service_date,
            quadrant=quadrant,
            provider_id=provider_id,
            procedure_id=procedure_id,
            plan_id=plan_id,
            subscriber_id=subscriber_id,
            provider_fees=provider_fees,
            allowed_fees=allowed_fees,
            member_coinsurance=member_coinsurance,
            member_copay=member_copay,
            net_fee=net_fee
        )
        session.add(claim)
        session.commit()
        session.refresh(claim)
        return claim

    @classmethod
    def get_top_net_fees_claims(cls, session: Session):
        return (
            session.query(Claim)
            .distinct(Claim.provider_id)
            .order_by(Claim.net_fee.desc())
            .limit(10)
            .all()
        )