from typing import List

from sqlalchemy.orm import Session

from claims.clients.payment_service_client import PaymentServiceClient
from claims.constants.notifying_status import NotifyingStatus
from claims.models.claims import Claim
from claims.models.payment_service_data import PaymentServiceData
from claims.models.plans import Plan
from claims.models.procedures import Procedure
from claims.models.providers import Provider
from claims.models.subscribers import Subscriber
from claims.types.request.create_claim import CreateClaim


class ClaimService:
    def __init__(self, session: Session):
        self.session = session

    def create_claim(self, claim_data: CreateClaim):
        procedure_id = Procedure.get_or_create_procedure(
            session=self.session,
            code=claim_data.submitted_procedure
        ).id
        provider_id = Provider.get_or_create_provider(
            session=self.session,
            npi=claim_data.provider_npi
        ).id
        plan_id = Plan.get_or_create_plan(
            session=self.session,
            plan_group=claim_data.plan_group
        ).id
        subscriber_id = Subscriber.get_or_create_subscriber(
            session=self.session,
            subscriber_number=claim_data.subscriber
        ).id
        net_fee = (claim_data.provider_fees + claim_data.member_coinsurance +
                   claim_data.member_copay - claim_data.allowed_fees)
        claim = Claim.create_claim(
            session=self.session, service_date=claim_data.service_date,
            quadrant=claim_data.quadrant, provider_id=provider_id, plan_id=plan_id,
            procedure_id=procedure_id, subscriber_id=subscriber_id, provider_fees=claim_data.provider_fees,
            allowed_fees=claim_data.allowed_fees, member_copay=claim_data.member_copay,
            member_coinsurance=claim_data.member_coinsurance, net_fee=net_fee
        )
        return claim.id, claim.net_fee

    def notify_payment_service(self, payment_data: List):
        response = PaymentServiceClient().notify_net_fee(payment_data=payment_data)
        if response.status_code == 200:
            notifying_status = NotifyingStatus.SUCCESS.value
        else:
            notifying_status = NotifyingStatus.FAILED.value

        for payment in payment_data:
            PaymentServiceData.create_payment_service_data(
                session=self.session,
                claim_id=payment['claim_id'],
                net_fee=payment['net_fee'],
                notifying_status=notifying_status
            )

