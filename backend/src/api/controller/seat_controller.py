from datetime import datetime
import random
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from api.controller.person_controller import subtract_credits
from api.model.seat_model import SeatResponse, SeatStatus
from api.view.seat_view import seat_by_id, filter_seats, occupy_seat_sql, free_seat_sql

from config.db_config import get_db
import structlog

_LOGGER = structlog.get_logger()

OCCUPY_SECONDS_MIN = 10
OCCUPY_SECONDS_VARIANCE = 5
OCCUPY_SECONDS_SNACK = 10

ORDER_COST = 10.0

router = APIRouter(
    prefix="/seat",
    tags=["Seats"]
)

# Helper function for looking up a seat 
def lookup_seat(seat_id: int, db) -> SeatResponse:
    row = db.execute(
        seat_by_id, 
        [seat_id]
    ).fetchone()

    if row is None:
        _LOGGER.warning(
            "seat_not_found",
            seat_id=seat_id
        )
        raise ValueError("Seat not found")

    _LOGGER.info(
        "seat_lookup",
        seat_id=seat_id
    )
    
    return SeatResponse(**row)

@router.get("/{seat_id}", response_model=SeatResponse)
def get_seat(seat_id: int, db=Depends(get_db)):
    """Fetches the seat with id=seat_id"""
    result = lookup_seat(seat_id, db)

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

    _LOGGER.info(
        "get_filtered_seats",
        table_id=table_id, 
        status=status, 
        person_id=person_id,         
        expires_before=expires_before,
        expires_after=expires_after,
        num_found=len(result)
    )

    return result

# A helper function that fetches all the seats where the person is seated at
def lookup_seat_by_person(person_id: int, db) -> Optional[SeatResponse]:
    query, params = filter_seats(person_id=person_id)
    existing_seats = db.execute(query, params).fetchall()

    if existing_seats:
        return SeatResponse(**existing_seats[0])
        
    return None

# The business logic for the occupy_seat endpoint
# Separate because it will be reused else where
def occupy_seat_now(seat_id: int, person_id: int, db) -> SeatResponse:
    existing_seat = lookup_seat_by_person(person_id, db)

    # checks if the person doesn't occupy another seat already
    if existing_seat:
        _LOGGER.warning(
            "person_already_seated",
            person_id=person_id,
            attempted_seat_id=seat_id,
            existing_seat_id=existing_seat.id
        )
        raise ValueError("Person is already seated elsewhere")

    seat = lookup_seat(seat_id, db)

    if seat.status != SeatStatus.free:
        _LOGGER.warning(
            "seat_not_free",
            seat_id=seat.id,
            seat_status=seat.status,
            occupying_person_id=seat.person_id,
            requesting_person_id=person_id,
            free_at=seat.expires_at
        )
        raise ValueError("Seat is not free")

    bonus_snack = subtract_credits(person_id, ORDER_COST, db)

    occupy_seconds = OCCUPY_SECONDS_MIN + random.randint(0, OCCUPY_SECONDS_VARIANCE)
    
    if bonus_snack:
        temp = occupy_seconds
        occupy_seconds += OCCUPY_SECONDS_SNACK
        _LOGGER.info(
            "bonus_snack_assigned",
            to_person_id=person_id,
            extra_time=occupy_seconds - temp,
            at_seat_id=seat.id,
            at_table_id=seat.table_id,
        )

    result = db.execute(
        occupy_seat_sql,
        (person_id, occupy_seconds, seat_id),
    ).fetchone()

    seat_result = SeatResponse(**result)

    _LOGGER.info(
        "seat_occupied",
        by_person_id=seat_result.person_id,
        seat_id=seat_id,
        at_table_id=seat_result.table_id,
        for_seconds=occupy_seconds,
    )

    db.commit()
    return seat_result

@router.put("/occupy/{seat_id}", response_model=SeatResponse)
def occupy_seat(seat_id: int, person_id:int, db=Depends(get_db)):
    """
        Updates the seat's status to occupied, inserts the occupying person's id
        and sets the expiration date.
        Also handles the bonus snacks and the duration of occupation.
        On success returns the updated seat's data.
    """
    try:
        return occupy_seat_now(seat_id, person_id, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Free seat up
@router.put("/free/{seat_id}", response_model=SeatResponse)
def free_seat(seat_id: int, db=Depends(get_db)):
    """
        Frees an occupied seat by returning its status to free. 
        Resets the person_id and expires_at to NULL.
        On success return the updated seat.
    """
    try:
        seat = lookup_seat(seat_id, db)

        result = db.execute(
            free_seat_sql,
            [seat.id],
        ).fetchone()

        _LOGGER.info(
            "seat_freed",
            seat_id=seat.id,
            old_status=seat.status,
            new_status=result.status
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
