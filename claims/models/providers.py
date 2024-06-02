from typing import List
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

    @classmethod
    def get_or_create_provider(cls, session: Session, npi: int):
        provider = session.query(Provider).filter_by(npi=npi).first()
        if provider is None:
            provider = Provider(npi=npi)
            session.add(provider)
            session.commit()
            session.refresh(provider)
        return provider

    @classmethod
    def get_providers_by_ids(cls, session: Session, provider_ids: List[int]):
        return (
            session.query(Provider).filter(Provider.id.in_(provider_ids)).all()
        )
