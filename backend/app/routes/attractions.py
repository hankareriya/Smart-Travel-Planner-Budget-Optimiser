from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import SessionLocal

from app.models import (
    Attraction,
    Destination
)

from app.schemas.attractions import (
    AttractionResponse
)


router = APIRouter(
    prefix="/attractions",
    tags=["Attractions"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get(
    "",
    response_model=list[AttractionResponse]
)
def get_attractions(
    db: Session = Depends(get_db)
):
    return db.query(
        Attraction
    ).all()


@router.get(
    "/{destination_id}",
    response_model=list[AttractionResponse]
)
def get_attractions_by_destination(
    destination_id: int,
    db: Session = Depends(get_db)
):
    destination = db.query(
        Destination
    ).filter(
        Destination.id
        == destination_id
    ).first()

    if destination is None:
        raise HTTPException(
            status_code=404,
            detail="Destination not found"
        )

    return db.query(
        Attraction
    ).filter(
        Attraction.destination_id
        == destination_id
    ).all()