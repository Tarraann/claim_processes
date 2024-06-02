from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional
from datetime import datetime
import re


def normalize_key(key: str) -> str:
    return key.lower().replace(' ', '_')


class CreateClaim(BaseModel):
    service_date: datetime
    submitted_procedure: str
    quadrant: Optional[str]
    plan_group: str
    subscriber: int
    provider_npi: int
    provider_fees: float
    allowed_fees: float
    member_coinsurance: float
    member_copay: float

    class Config:
        alias_generator = normalize_key
        allow_population_by_field_name = True
        orm_mode = True
        schema_extra = {
            "example": [
                {
                    "Service Date": "3/28/2018 0:00:00",
                    "Submitted Procedure": "D0180",
                    "Quadrant": "UR",
                    "Plan Group": "GRP-1000",
                    "Subscriber": 3730189502,
                    "Provider NPI": 1497775530,
                    "Provider Fees": 100.00,
                    "Allowed Fees": 100.00,
                    "Member Coinsurance": 0.00,
                    "Member Copay": 0.00,
                }
            ]
        }

    @validator('submitted_procedure')
    def validate_submitted_procedure(cls, v):
        if not v.startswith('D'):
            raise ValueError('submitted_procedure must start with the letter D')
        return v

    @validator('provider_npi')
    def validate_provider_npi(cls, v):
        if not (isinstance(v, int) and len(str(v)) == 10):
            raise ValueError('provider_npi must be a 10-digit integer')
        return v

    @root_validator(pre=True)
    def convert_service_date(cls, values):
        service_date_str = values.get('service_date')
        if service_date_str:
            try:
                values['service_date'] = datetime.strptime(service_date_str, '%m/%d/%Y %H:%M:%S')
            except ValueError:
                raise ValueError('service_date must be in the format MM/DD/YYYY HH:MM:SS')
        return values
