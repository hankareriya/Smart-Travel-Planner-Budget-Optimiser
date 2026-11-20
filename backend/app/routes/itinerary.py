from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.models.trips import Trip
from app.models.destinations import Destination
from app.models.attractions import Attraction
from app.models.itinerary_items import ItineraryItem

from app.routes.auth import get_current_user

from app.services.itinerary_service import (
    generate_trip_itinerary,
    calculate_fixed_budget
)


router = APIRouter(
    prefix="/trips",
    tags=["Itinerary"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def serialize_time(value):
    if value is None:
        return None

    return value.strftime(
        "%H:%M"
    )


@router.get(
    "/{trip_id}/itinerary"
)
def get_itinerary(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    trip = db.query(
        Trip
    ).filter(
        Trip.id == trip_id,
        Trip.user_id == current_user.id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found."
        )

    destination = db.query(
        Destination
    ).filter(
        Destination.id == trip.destination_id
    ).first()

    items = db.query(
        ItineraryItem
    ).filter(
        ItineraryItem.trip_id == trip.id
    ).order_by(
        ItineraryItem.day.asc(),
        ItineraryItem.order_number.asc()
    ).all()

    attraction_ids = set()

    for item in items:

        if item.attraction_id:
            attraction_ids.add(
                item.attraction_id
            )

        if item.from_attraction_id:
            attraction_ids.add(
                item.from_attraction_id
            )

        if item.to_attraction_id:
            attraction_ids.add(
                item.to_attraction_id
            )

    attractions = {}

    if attraction_ids:

        rows = db.query(
            Attraction
        ).filter(
            Attraction.id.in_(
                attraction_ids
            )
        ).all()

        attractions = {
            row.id: row
            for row in rows
        }

    days_map = {}

    for item in items:

        attraction = attractions.get(
            item.attraction_id
        )

        from_attraction = attractions.get(
            item.from_attraction_id
        )

        to_attraction = attractions.get(
            item.to_attraction_id
        )

        activity = {
            "id": item.id,
            "item_type": item.item_type,

            "attraction_id":
                item.attraction_id,

            "name":
                attraction.name
                if attraction
                else None,

            "category":
                attraction.category
                if attraction
                else None,

            "rating":
                attraction.rating
                if attraction
                else None,

            "price":
                attraction.price
                if attraction
                and item.item_type == "attraction"
                else 0,

            "duration":
                attraction.duration
                if attraction
                else None,

            "place_type":
                attraction.place_type
                if attraction
                else None,

            "start_time":
                serialize_time(
                    item.start_time
                ),

            "end_time":
                serialize_time(
                    item.end_time
                ),

            "time":
                (
                    f"{serialize_time(item.start_time)}"
                    f" – "
                    f"{serialize_time(item.end_time)}"
                )
                if item.start_time
                and item.end_time
                else "",

            "distance_km":
                item.distance_km or 0,

            "travel_time_minutes":
                item.travel_time_minutes or 0,

            "travel_cost":
                item.travel_cost or 0,

            "transport_mode":
                item.transport_mode,

            "meal_type":
                item.meal_type,

            "notes":
                item.notes,

            "from_name":
                from_attraction.name
                if from_attraction
                else None,

            "to_name":
                to_attraction.name
                if to_attraction
                else None
        }

        days_map.setdefault(
            item.day,
            []
        ).append(
            activity
        )

    days = []

    total_local_transport = 0
    total_activities = 0

    for day_number in sorted(
        days_map.keys()
    ):

        activities = days_map[
            day_number
        ]

        day_local_transport = 0
        day_activity_cost = 0

        for activity in activities:

            if activity[
                "item_type"
            ] == "travel":

                day_local_transport += float(
                    activity[
                        "travel_cost"
                    ] or 0
                )

            elif activity[
                "item_type"
            ] == "attraction":

                day_activity_cost += (
                    float(
                        activity[
                            "price"
                        ] or 0
                    )
                    * trip.travelers
                )

        total_local_transport += (
            day_local_transport
        )

        total_activities += (
            day_activity_cost
        )

        days.append(
            {
                "day": day_number,
                "activities": activities,
                "local_transportation":
                    round(
                        day_local_transport,
                        2
                    ),
                "activities_cost":
                    round(
                        day_activity_cost,
                        2
                    )
            }
        )

    number_of_days = (
        trip.end_date
        - trip.start_date
    ).days + 1

    fixed = calculate_fixed_budget(
        trip,
        number_of_days
    )

    planned = (
        fixed["accommodation"]
        + fixed["intercity_transportation"]
        + fixed["food"]
        + total_activities
        + total_local_transport
        + fixed["miscellaneous"]
    )

    total_budget = float(
        trip.budget or 0
    )

    remaining = (
        total_budget
        - planned
    )

    percentage = (
        planned / total_budget * 100
        if total_budget > 0
        else 0
    )

    return {
        "trip_id":
            trip.id,

        "destination":
            destination.name
            if destination
            else "Unknown Destination",

        "destination_id":
            trip.destination_id,

        "start_date":
            str(trip.start_date),

        "end_date":
            str(trip.end_date),

        "travelers":
            trip.travelers,

        "optimization":
            trip.optimization_mode,

        "interests":
            trip.interests or [],

        "days":
            days,

        "budget":
            {
                "total_budget":
                    total_budget,

                "accommodation":
                    round(
                        fixed[
                            "accommodation"
                        ],
                        2
                    ),

                "intercity_transportation":
                    round(
                        fixed[
                            "intercity_transportation"
                        ],
                        2
                    ),

                "food":
                    round(
                        fixed["food"],
                        2
                    ),

                "activities":
                    round(
                        total_activities,
                        2
                    ),

                "local_transportation":
                    round(
                        total_local_transport,
                        2
                    ),

                "miscellaneous":
                    round(
                        fixed[
                            "miscellaneous"
                        ],
                        2
                    ),

                "planned":
                    round(
                        planned,
                        2
                    ),

                "remaining":
                    round(
                        remaining,
                        2
                    ),

                "percentage":
                    round(
                        percentage,
                        2
                    ),

                "over_budget":
                    planned > total_budget
            }
    }