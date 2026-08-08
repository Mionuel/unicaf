from fastapi import APIRouter, Depends, HTTPException

from api.controller.seat_controller import lookup_seat
from api.model.reservation_model import ReservationResponse
from api.model.seat_model import SeatStatus
from api.view.reservation_view import fetch_reservation_by_seat, insert_reservation

from config.db_config import get_db

router = APIRouter(
    prefix="/reservation",
    tags=["Reservation"]
)

# A helper function that checks if the seat with seat_id is already reserved
def is_reserved(seat_id: int, db) -> bool:
    row = db.execute(
        fetch_reservation_by_seat, 
        [seat_id]
    ).fetchone()

    if row is None:
        return False

    return True

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
        raise HTTPException(status_code=400, detail="Cannot reserve a free seat")

    if is_reserved(seat_id, db):
        raise HTTPException(status_code=409, detail="Seat is already reserved")

    result = db.execute(
        insert_reservation, 
        (seat_id, person_id)
    ).fetchone()

    return result
