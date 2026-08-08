from datetime import datetime
from pydantic import BaseModel

class ReservationResponse(BaseModel):
    id: int
    seat_id: int
    person_id: int
