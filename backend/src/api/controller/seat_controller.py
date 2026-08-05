from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from api.model.seat_model import SeatResponse, SeatStatus
from api.view.seat_view import seat_by_id, filter_seats

from config.db_config import get_db

router = APIRouter(
    prefix="/seat",
    tags=["Seats"]
)

@router.get("/{seat_id}", response_model=SeatResponse)
def get_seat(seat_id: int, db=Depends(get_db)):
    """Fetches the seat with id=seat_id"""
    result = db.execute(
        seat_by_id,
        [seat_id]
    ).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Seat not found")

    return result

@router.get("/", response_model=List[SeatResponse])
def get_seats(
    table_id: Optional[int] = Query(None, description="Filter by table"),
    status: Optional[SeatStatus] = Query(None, description="Filter by seat status"),
    person_id: Optional[int] = Query(None, description="Filter by assigned person"),
    expires_before: Optional[datetime] = Query(None, description="Filter before the specified date"),
    expires_after: Optional[datetime] = Query(None, description="Filter after the specified date"),
    db=Depends(get_db),
):
    """
    Fetches seats optionally filtered by table_id / status / person_id.
    If no filters are provided, returns all seats
    """
    query, params = filter_seats(
        table_id=table_id, 
        status=status, 
        person_id=person_id,         
        expires_before=expires_before,
        expires_after=expires_after
    )

    result = db.execute(query, params).fetchall()

    return result
