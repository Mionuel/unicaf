from typing import List

from fastapi import APIRouter, Depends, HTTPException

from api.controller.queue_controller import dequeue
from api.controller.reservation_controller import delete_reservation, fetch_reservation
from api.controller.seat_controller import occupy_seat_now
from api.model.seat_model import SeatResponse

from api.view.seat_view import free_expired_seats_sql
from config.db_config import get_db

import structlog

_LOGGER = structlog.get_logger()

router = APIRouter(
    prefix="/state",
    tags=["State"]
)


def free_expired_seats(db) -> List[SeatResponse] | None:
    rows = db.execute(
        free_expired_seats_sql
    ).fetchall()

    if not rows:
        return None

    # converts dicts to SeatResponse objects
    return [SeatResponse(**row) for row in rows]

# Updates the seat's state following one of 2 cases:
# 1. if the seat has a reservation on it 
#   => immediately let the person, who did the reservation, occupy that seat
#   => delete the reservation
#   => update seat's state to occupied (call the occupy_now function on it)

# 2. if the seat has no reservations 
#   => dequeue (a function) the first person from the queue
#   => call occupy now on that seat
def update_seat(seat_id:int, db) -> None:
    reservation = fetch_reservation(seat_id, db)

    person_id = None

    # if there was a reservation => get person_id from the reservation 
    # so that the person can immediately occupy the seat in question
    if reservation is not None:
        delete_reservation(reservation.id, db)
        person_id = reservation.person_id
        _LOGGER.info(
            "reservation_executed",
            for_person_id=person_id,
            at_seat_id=reservation.seat_id
        )

    # if there was no reservation for this seat => dequeue the first person and seat them
    else:
        queue_entry = dequeue(db)

        # the queue is empty
        if queue_entry is None:
            return

        person_id = queue_entry.person_id

        _LOGGER.info(
            "dequeued",
            person_id=person_id,
            joined_at=queue_entry.joined_at
        )

    # If the queue is empty / there are no reservations => return
    if person_id is None:
        return

    # ensures that if the person cannot be seated they get removed from the queue
    # instead of occupying it indefinitely
    db.commit()
    
    try:
        occupy_seat_now(seat_id, person_id, db)
    except ValueError as e:
        print(str(e))
        # The person cannot be seated (not enough credits, seat taken, etc.) => try the next one
        update_seat(seat_id, db)

# Looks up expired seats and calls update_seat on them
def update_all_seats(db) -> List[SeatResponse] | None:
    expired_seats = free_expired_seats(db)

    # no expired seats => return
    if expired_seats is None:
        return

    # update the state of each seat according to 
    for seat in expired_seats:
        update_seat(seat.id, db)

    _LOGGER.info(
        "seats_updated",
        number_seats=len(expired_seats)
    )

    return expired_seats

@router.post("/", response_model=List[SeatResponse] | None)
def update(db=Depends(get_db)):
    try:
        return update_all_seats(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
