from typing import List

from fastapi import APIRouter, Depends
from psycopg import Connection

from config.db_config import get_db

from api.model.queue_model import QueueEntry
from api.view.queue_view import enqueue_sql, dequeue_sql, queue_entries_sql, person_already_in_queue

router = APIRouter(
    prefix="/queue",
    tags=["Queue"]
)

import structlog

_LOGGER = structlog.get_logger()

def is_person_enqueued(person_id: int, db):
    exists = db.execute(
        person_already_in_queue, 
        [person_id]
    ).fetchone()
    
    return exists

# Business logic for enqueueing a person
# Separate because it will be reused elsewhere (e.g. simulation_controller)
def enqueue_now(person_id: int, db) -> QueueEntry | None:
    entry = db.execute(
        enqueue_sql,
        [person_id]
    ).fetchone()

    if is_person_enqueued:
        _LOGGER.warning(
            "already_in_queue", 
            person_id=person_id
        )
        return None

    queue_entry = QueueEntry(**entry)

    _LOGGER.info(
        "enqueued",
        person_id=queue_entry.person_id,
        entry_id=queue_entry.id,
        joined_at=queue_entry.joined_at
    )

    return queue_entry


@router.post("/enqueue", response_model=QueueEntry | None)
def enqueue(person_id: int, db=Depends(get_db)):
    return enqueue_now(person_id, db)

# Dequeues the first person in the queue
def dequeue(db) -> QueueEntry | None:
    entry = db.execute(
        dequeue_sql
    ).fetchone()

    if entry is None:
        return None

    return QueueEntry(**entry)

def list_queue_now(db: Connection) -> List[QueueEntry]:
    rows = db.execute(
        queue_entries_sql
    ).fetchall()

    entries = [QueueEntry.model_validate(row) for row in rows]

    return entries

# Returns all the queue entries as a List
@router.get("/all", response_model=List[QueueEntry])
def list_queue(db=Depends(get_db)):
    """Fetches the current queue"""
    entries = list_queue_now(db)

    _LOGGER.info(
        "fetched_queue_entries",
        num_entries = len(entries)
    )

    return entries
