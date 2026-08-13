from typing import List

from fastapi import APIRouter, Depends

from config.db_config import get_db

from api.model.queue_model import QueueEntry
from api.view.queue_view import enqueue_sql, dequeue_sql, queue_entries_sql

router = APIRouter(
    prefix="/queue",
    tags=["Queue"]
)

# Enqueues a person
@router.post("/enqueue", response_model=QueueEntry | None)
def enqueue(person_id: int, db=Depends(get_db)):
    entry = db.execute(
        enqueue_sql,
        [person_id]
    ).fetchone()

    if entry is None:
        return None

    return QueueEntry(**entry)

# Dequeues the first person in the queue
def dequeue(db) -> QueueEntry | None:
    entry = db.execute(
        dequeue_sql
    ).fetchone()

    if entry is None:
        return None

    print(entry)

    return QueueEntry(**entry)

# Returns all the queue entries as a List
@router.get("/all", response_model=List[QueueEntry])
def list_queue(db=Depends(get_db)):
    """Fetches the current queue"""
    rows = db.execute(queue_entries_sql).fetchall()
    return [QueueEntry(**row) for row in rows]
