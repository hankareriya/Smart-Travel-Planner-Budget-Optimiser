from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Date,
    ForeignKey,
    JSON
)

from app.database.database import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    destination_id = Column(
        Integer,
        ForeignKey("destinations.id"),
        nullable=False
    )

    start_date = Column(
        Date,
        nullable=False
    )

    end_date = Column(
        Date,
        nullable=False
    )

    travelers = Column(
        Integer,
        nullable=False
    )

    budget = Column(
        Float
    )

    interests = Column(
        JSON,
        nullable=True
    )

    optimization_mode = Column(
        String(50)
    )

    food_budget_per_person = Column(
        Float,
        default=0
    )

    accommodation_per_night = Column(
        Float,
        default=0
    )

    intercity_transportation_cost = Column(
        Float,
        default=0
    )

    miscellaneous_budget = Column(
        Float,
        default=0
    )

    transport_mode = Column(
        String(50),
        default="car"
    )