from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import (
    Base,
    engine,
    SessionLocal
)


from app.routes.auth import (
    router as auth_router
)

from app.routes.trips import (
    router as trips_router
)

from app.routes.attractions import (
    router as attractions_router
)

from app.routes.destinations import (
    router as destinations_router
)

from app.routes.itinerary import (
    router as itinerary_router
)

from app.models import (
    User,
    Destination,
    Attraction,
    Trip,
    ItineraryItem
)


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Smart Travel Planner API"
)


app.include_router(
    destinations_router
)

app.include_router(
    attractions_router
)

app.include_router(
    auth_router
)

app.include_router(
    trips_router
)

app.include_router(
    itinerary_router
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {
        "message":
            "Smart Travel Planner API"
    }


