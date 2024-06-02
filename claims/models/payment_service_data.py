from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import Session

from claims.constants.notifying_status import NotifyingStatus
from claims.lib.logger import logger
from claims.models.base_model import DBBaseModel


class PaymentServiceData(DBBaseModel):
    __tablename__ = "payment_service_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    claim_id = Column(Integer, nullable=False)
    net_fee = Column(Float, nullable=False)
    notifying_status = Column(String, nullable=False)

    @classmethod
    def create_payment_service_data(cls, session: Session, claim_id: int, net_fee: float, notifying_status: str):
        payment_service_data = PaymentServiceData(
            claim_id=claim_id,
            net_fee=net_fee,
            notifying_status=notifying_status
        )
        session.add(payment_service_data)
        session.commit()

    @classmethod
    def get_failed_notifying_status(cls, session: Session):
        return (
            session.query(PaymentServiceData)
            .filter(PaymentServiceData.notifying_status == NotifyingStatus.FAILED.value)
            .all()
        )

    @classmethod
    def update_notifying_status(cls, session: Session, id: int, notifying_status: str):
        data = session.query(PaymentServiceData).filter(PaymentServiceData.id == id).first()
        if data is None:
            logger.info("No data found in Payment Service Data table for the id: {}".format(id))
            return
        data.notifying_status = notifying_status
        session.flush()
