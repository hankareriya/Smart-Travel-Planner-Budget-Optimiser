from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from datetime import date
from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.models import (
    User,
    Trip,
    Destination,
    ItineraryItem
)

from app.schemas.trips import (
    TripCreate,
    TripUpdate,
    TripResponse
)

from app.routes.auth import (
    get_current_user
)

from app.services.itinerary_service import (
    generate_trip_itinerary
)


router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


def build_trip_response(
    db,
    trip
):
    destination = db.query(
        Destination
    ).filter(
        Destination.id
        == trip.destination_id
    ).first()

    has_itinerary = db.query(
        ItineraryItem
    ).filter(
        ItineraryItem.trip_id
        == trip.id
    ).first() is not None

    return {
        "id": trip.id,
        "user_id": trip.user_id,
        "destination_id":
            trip.destination_id,

        "start_date":
            trip.start_date,

        "end_date":
            trip.end_date,

        "travelers":
            trip.travelers,

        "budget":
            trip.budget,

        "interests":
            trip.interests or [],

        "optimization_mode":
            trip.optimization_mode,

        "food_budget_per_person":
            trip.food_budget_per_person or 0,

        "accommodation_per_night":
            trip.accommodation_per_night or 0,

        "intercity_transportation_cost":
            trip.intercity_transportation_cost
            or 0,

        "miscellaneous_budget":
            trip.miscellaneous_budget
            or 0,

        "transport_mode":
            trip.transport_mode
            or "car",

        "destination_name":
            destination.name
            if destination
            else "Unknown Destination",

        "itinerary_generated":
            has_itinerary,

        "has_itinerary":
            has_itinerary
    }


@router.post(
    "",
    response_model=TripResponse
)
def create_trip(
    trip_data: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    destination = db.query(
        Destination
    ).filter(
        Destination.id
        == trip_data.destination_id
    ).first()

    if not destination:
        raise HTTPException(
            status_code=404,
            detail="Destination not found."
        )

    if trip_data.end_date < trip_data.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date."
        )

    if trip_data.travelers < 1:
        raise HTTPException(
            status_code=400,
            detail="Travelers must be at least 1."
        )

    trip = Trip(
        user_id=current_user.id,
        destination_id=
            trip_data.destination_id,
        start_date=
            trip_data.start_date,
        end_date=
            trip_data.end_date,
        travelers=
            trip_data.travelers,
        budget=
            trip_data.budget,
        interests=
            trip_data.interests or [],
        optimization_mode=
            trip_data.optimization_mode
            or "best experience",

        food_budget_per_person=
            trip_data.food_budget_per_person
            or 0,

        accommodation_per_night=
            trip_data.accommodation_per_night
            or 0,

        intercity_transportation_cost=
            trip_data.intercity_transportation_cost
            or 0,

        miscellaneous_budget=
            trip_data.miscellaneous_budget
            or 0,

        transport_mode=
            trip_data.transport_mode
            or "car"
    )

    db.add(trip)
    db.commit()
    db.refresh(trip)

    return build_trip_response(
        db,
        trip
    )


@router.get(
    "",
    response_model=list[TripResponse]
)
def get_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    trips = db.query(
        Trip
    ).filter(
        Trip.user_id == current_user.id
    ).order_by(
        Trip.start_date.asc()
    ).all()

    today = date.today()

    # =====================================================
    # AUTOMATICALLY GENERATE ITINERARY FOR PREVIOUS TRIPS
    # =====================================================

    for trip in trips:

        # Only previous trips
        if trip.start_date < today:

            # Check whether itinerary already exists
            has_itinerary = db.query(
                ItineraryItem
            ).filter(
                ItineraryItem.trip_id == trip.id
            ).first() is not None

            # If previous trip has no itinerary,
            # generate it automatically in the backend.
            if not has_itinerary:

                try:

                    generate_trip_itinerary(
                        db,
                        trip.id
                    )

                except ValueError as error:

                    # Do not stop the entire dashboard
                    # if one old trip cannot be generated.
                    print(
                        f"Could not generate itinerary "
                        f"for previous trip {trip.id}: "
                        f"{error}"
                    )

    # =====================================================
    # RETURN UPDATED TRIPS
    # =====================================================

    return [
        build_trip_response(
            db,
            trip
        )
        for trip in trips
    ]


@router.put(
    "/{trip_id}",
    response_model=TripResponse
)
def update_trip(
    trip_id: int,
    trip_data: TripUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    trip = db.query(
        Trip
    ).filter(
        Trip.id == trip_id,
        Trip.user_id
        == current_user.id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found."
        )

    update_data = trip_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            trip,
            key,
            value
        )

    if (
        trip.end_date
        < trip.start_date
    ):
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date."
        )

    db.query(
        ItineraryItem
    ).filter(
        ItineraryItem.trip_id
        == trip.id
    ).delete(
        synchronize_session=False
    )

    db.commit()
    db.refresh(trip)

    return build_trip_response(
        db,
        trip
    )


@router.delete(
    "/{trip_id}"
)
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    trip = db.query(
        Trip
    ).filter(
        Trip.id == trip_id,
        Trip.user_id
        == current_user.id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found."
        )

    db.query(
        ItineraryItem
    ).filter(
        ItineraryItem.trip_id
        == trip.id
    ).delete(
        synchronize_session=False
    )

    db.delete(trip)
    db.commit()

    return {
        "message":
            "Trip deleted successfully."
    }


@router.post(
    "/{trip_id}/generate"
)
def generate_itinerary(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    trip = db.query(
        Trip
    ).filter(
        Trip.id == trip_id,
        Trip.user_id
        == current_user.id
    ).first()

    if not trip:
        raise HTTPException(
            status_code=404,
            detail="Trip not found."
        )

    try:

        result = generate_trip_itinerary(
            db,
            trip_id
        )

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )