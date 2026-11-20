from typing import Optional

from pydantic import BaseModel


class AttractionResponse(BaseModel):
    id: int
    destination_id: int
    name: str
    category: Optional[str] = None
    place_type: Optional[str] = "ATTRACTION"
    rating: Optional[float] = None
    price: Optional[float] = 0
    duration: Optional[float] = 1
    popularity: Optional[float] = 50
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    opening_time: Optional[str] = None
    closing_time: Optional[str] = None

    class Config:
        from_attributes = True