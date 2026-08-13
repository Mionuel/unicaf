from datetime import datetime
from pydantic import BaseModel

class QueueEntry(BaseModel):
    id: int
    person_id: int
    joined_at: datetime
