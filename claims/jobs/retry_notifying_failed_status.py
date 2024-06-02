from claims.clients.payment_service_client import PaymentServiceClient
from claims.constants.notifying_status import NotifyingStatus
from claims.models.payment_service_data import PaymentServiceData
from sqlalchemy.orm import Session


def retry_notifying_failed_status(session: Session):
    failed_status_payment_data = PaymentServiceData.get_failed_notifying_status(session=session)
    payment_data = []
    for payment in failed_status_payment_data:
        payment_data.append({
            'claim_id': payment.claim_id,
            'net_fee': payment.net_fee
        })
    response = PaymentServiceClient().notify_net_fee(payment_data=payment_data)
    if response.status_code == 200:
        notifying_status = NotifyingStatus.SUCCESS.value
    else:
        notifying_status = NotifyingStatus.FAILED.value
    for payment in failed_status_payment_data:
        PaymentServiceData.update_notifying_status(
            session=session,
            id=payment.id,
            notifying_status=notifying_status
        )
