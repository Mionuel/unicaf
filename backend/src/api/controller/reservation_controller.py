from fastapi import APIRouter, Depends, HTTPException

from api.controller.seat_controller import lookup_seat
from api.model.reservation_model import ReservationResponse
from api.model.seat_model import SeatStatus
from api.view.reservation_view import fetch_reservation_by_seat, insert_reservation, delete_reservation_by_id

from config.db_config import get_db

router = APIRouter(
    prefix="/reservation",
    tags=["Reservation"]
)

import structlog

_LOGGER = structlog.get_logger()

# A helper function that checks if the seat with seat_id is already reserved
# On success returns reservation's id else - None
def fetch_reservation(seat_id: int, db) -> ReservationResponse | None:
    row = db.execute(
        fetch_reservation_by_seat, 
        [seat_id]
    ).fetchone()

    if row is None:
        return None

    reservation = ReservationResponse(**row)

    return reservation

# Reserve a seat
@router.post("/{seat_id}", response_model=ReservationResponse)
def reserve_seat(seat_id: int, person_id: int, db=Depends(get_db)):
    """
        Creates a reservation for an occupied seat. 
        If the seat is free then the call raises an exception.
        On success return the created reservation.
    """
    try:
        seat = lookup_seat(seat_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # TODO: A free seat should be occupied directly without a reservation
    if seat.status is SeatStatus.free:
        _LOGGER.warning(
            "reservation_free_seat",
            seat_id=seat.id
        )
        raise HTTPException(status_code=400, detail="Cannot reserve a free seat")

    # if there was a reservation already => error
    reservation = fetch_reservation(seat_id, db)

    if reservation is not None:
        _LOGGER.warning(
            "seat_already_reserved",
            seat_id=seat.id,
            seat_status=seat.status
        )
        raise HTTPException(status_code=409, detail="Seat is already reserved")

    result = db.execute(
        insert_reservation, 
        (seat_id, person_id)
    ).fetchone()

    return result

# Delete a reservation
def delete_reservation(reservation_id: int, db=Depends(get_db)):
    result = db.execute(
        delete_reservation_by_id, [reservation_id]
    ).fetchone()

    return result
