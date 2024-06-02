from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    success: bool
    message: str

    class Config:
        orm_mode = True