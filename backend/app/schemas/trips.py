from datetime import date
from typing import Optional, List

from pydantic import BaseModel


class TripCreate(BaseModel):
    destination_id: int
    start_date: date
    end_date: date
    travelers: int
    budget: Optional[float] = None
    interests: Optional[List[str]] = None
    optimization_mode: Optional[str] = "best experience"

    food_budget_per_person: Optional[float] = 0
    accommodation_per_night: Optional[float] = 0
    intercity_transportation_cost: Optional[float] = 0
    miscellaneous_budget: Optional[float] = 0
    transport_mode: Optional[str] = "car"


class TripUpdate(BaseModel):
    destination_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    travelers: Optional[int] = None
    budget: Optional[float] = None
    interests: Optional[List[str]] = None
    optimization_mode: Optional[str] = None

    food_budget_per_person: Optional[float] = None
    accommodation_per_night: Optional[float] = None
    intercity_transportation_cost: Optional[float] = None
    miscellaneous_budget: Optional[float] = None
    transport_mode: Optional[str] = None


class TripResponse(BaseModel):
    id: int
    user_id: int
    destination_id: int

    start_date: date
    end_date: date

    travelers: int
    budget: Optional[float]

    interests: Optional[List[str]]
    optimization_mode: Optional[str]

    food_budget_per_person: Optional[float] = 0
    accommodation_per_night: Optional[float] = 0
    intercity_transportation_cost: Optional[float] = 0
    miscellaneous_budget: Optional[float] = 0
    transport_mode: Optional[str] = "car"

    destination_name: Optional[str] = None

    itinerary_generated: bool = False
    has_itinerary: bool = False

    class Config:
        from_attributes = True