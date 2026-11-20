from pydantic import BaseModel


class DestinationResponse(BaseModel):
    id: int
    name: str
    country: str

    class Config:
        from_attributes = True