from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models import Destination
from app.schemas.destinations import DestinationResponse


router = APIRouter(
    prefix="/destinations",
    tags=["Destinations"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get(
    "",
    response_model=list[DestinationResponse]
)
def get_destinations(
    db: Session = Depends(get_db)
):

    destinations = db.query(Destination).all()

    return destinations