from pydantic import BaseModel


class GetTopProvidersResponse(BaseModel):
    provider_id: int
    provider_npi: int
    net_fee: float

    class Config:
        orm_mode = True
