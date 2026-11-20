from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Time,
    ForeignKey
)

from app.database.database import Base


class ItineraryItem(Base):
    __tablename__ = "itinerary_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    trip_id = Column(
        Integer,
        ForeignKey("trips.id"),
        nullable=False
    )

    day = Column(
        Integer,
        nullable=False
    )

    item_type = Column(
        String(30),
        nullable=False,
        default="attraction"
    )

    attraction_id = Column(
        Integer,
        ForeignKey("attractions.id"),
        nullable=True
    )

    from_attraction_id = Column(
        Integer,
        ForeignKey("attractions.id"),
        nullable=True
    )

    to_attraction_id = Column(
        Integer,
        ForeignKey("attractions.id"),
        nullable=True
    )

    start_time = Column(
        Time
    )

    end_time = Column(
        Time
    )

    order_number = Column(
        Integer,
        default=1
    )

    distance_km = Column(
        Float,
        default=0
    )

    travel_time_minutes = Column(
        Integer,
        default=0
    )

    travel_cost = Column(
        Float,
        default=0
    )

    transport_mode = Column(
        String(50),
        nullable=True
    )

    meal_type = Column(
        String(50),
        nullable=True
    )

    notes = Column(
        String(255),
        nullable=True
    )