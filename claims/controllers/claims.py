from typing import List

from fastapi import APIRouter, HTTPException
from fastapi_sqlalchemy import db

from claims.models.claims import Claim
from claims.models.providers import Provider
from claims.services.claim_service import ClaimService
from claims.types.request.create_claim import CreateClaim
from claims.types.response.base_response_model import BaseResponseModel
from claims.lib.logger import logger
from claims.types.response.get_top_providers import GetTopProvidersResponse

router = APIRouter()


@router.post("/create", response_model=BaseResponseModel)
async def create_claims(claims: List[CreateClaim]):
    from claims.worker import notify_payments_service
    session = db.session
    try:
        logger.info(f"Creating {len(claims)} claims")
        payment_data = []
        claim_service = ClaimService(session=session)
        for claim in claims:
            claim_id, net_fee = claim_service.create_claim(claim)
            payment_data.append({"claim_id": claim_id, "net_fee": net_fee})
            logger.info(f"claim {claim_id} created with {net_fee} net fee")

        notify_payments_service(payment_data)
        return BaseResponseModel(
            success=True, message="Claims Created Successfully."
        )
    except Exception as e:
        logger.error(f"Error occurred while creating {len(claims)} claims --> {e}")
        raise HTTPException(status_code=500, detail=f"Error while creating claims {e}")


@router.get("/top/providers", response_model=List[GetTopProvidersResponse])
async def get_top_providers():
    session = db.session
    try:
        response = []
        top_net_fees_claims = Claim.get_top_net_fees_claims(session=session)
        provider_ids = [provider.id for provider in top_net_fees_claims]
        providers = Provider.get_providers_by_ids(session=session, provider_ids=provider_ids)
        for provider, claim in providers, top_net_fees_claims:
            response.append(
                GetTopProvidersResponse(
                    provider_id=provider.id,
                    provider_npi=provider.npi,
                    net_fee=claim.net_fee
                )
            )
        return response
    except Exception as e:
        logger.error(f"Error occurred while fetching top providers --> {e}")
        raise HTTPException(status_code=500, detail=f"Error while fetching top providers {e}")



