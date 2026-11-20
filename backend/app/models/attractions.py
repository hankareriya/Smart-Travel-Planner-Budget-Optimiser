from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Time,
    DECIMAL
)

from app.database.database import Base


class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    destination_id = Column(
        Integer,
        ForeignKey("destinations.id"),
        nullable=False
    )

    name = Column(
        String(150),
        nullable=False
    )

    category = Column(
        String(100)
    )

    place_type = Column(
        String(50),
        default="ATTRACTION",
        nullable=False
    )

    rating = Column(
        Float
    )

    price = Column(
        Float,
        default=0
    )

    duration = Column(
        Float
    )

    popularity = Column(
        Float,
        default=50
    )

    latitude = Column(
        DECIMAL(10, 7)
    )

    longitude = Column(
        DECIMAL(10, 7)
    )

    opening_time = Column(
        Time
    )

    closing_time = Column(
        Time
    )