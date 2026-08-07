from datetime import datetime
import random
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from api.controller.order_controller import ORDER_COST, insert_order
from api.controller.person_controller import subtract_credits
from api.model.seat_model import SeatOccupyPayload, SeatResponse, SeatStatus
from api.view.seat_view import seat_by_id, filter_seats, occupy_seat_sql

from config.db_config import get_db

OCCUPY_SECONDS_MIN = 10
OCCUPY_SECONDS_VARIANCE = 5
OCCUPY_SECONDS_SNACK = 10

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

# Helper function for looking up a seat
def lookup_seat(seat_id: int, db) -> SeatResponse:
    row = db.execute(
        seat_by_id, [seat_id]
    ).fetchone()

    if row is None:
        raise ValueError("Seat not found")
    
    return SeatResponse(**row)

# Occupy seat
@router.post("/occupy/{seat_id}", response_model=SeatResponse)
def occupy_seat(payload: SeatOccupyPayload, seat_id: int, db=Depends(get_db)):
    """ 
        Updates the seat's status to occupied, inserts the occupying person's id 
        and sets the expiration date.
        On Success returns the updated seat's data.
    """
    try:
        seat = lookup_seat(seat_id, db)

        if seat.status != SeatStatus.free:
            raise HTTPException(status_code=406, detail="Seat is not free")

        # Indicates that the person should receive a bonus snack
        bonus_snack = subtract_credits(payload.person_id, ORDER_COST, db)

        # The person will occupy the seat for 10 + rand(0, 5) seconds
        occupy_seconds = OCCUPY_SECONDS_MIN + random.randint(0, OCCUPY_SECONDS_VARIANCE)

        # If the person received a bonus snack => they will seat for longer
        if bonus_snack:
            occupy_seconds += OCCUPY_SECONDS_SNACK

        result = db.execute(
            occupy_seat_sql,
            (payload.person_id, occupy_seconds, seat_id),
        ).fetchone()

        # Saves the order into the Order table
        insert_order(payload.person_id, seat.id, bonus_snack, db)

        # The changes will take effect only if no errors occured, otherwise everything will be rolled back
        db.commit()

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Free seat up
