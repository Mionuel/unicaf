from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class SeatStatus(str, Enum):
    free = "free"
    reserved = "reserved"
    occupied = "occupied"

class SeatResponse(BaseModel):
    id: int
    table_id: int
    status: SeatStatus
    person_id: int | None = None
    expires_at: datetime | None = None

class SeatOccupyPayload(BaseModel):
    new_satus: SeatStatus
    person_id: int
    expires_at: datetime | None = None
