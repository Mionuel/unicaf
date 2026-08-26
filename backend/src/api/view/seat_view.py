from datetime import datetime

from api.model.seat_model import SeatStatus

seat_by_id = """
    SELECT *
    FROM "Seat"
    WHERE id = %s;
"""

all_seats = """
    SELECT 
        id, 
        table_id, 
        status, 
        person_id, 
        expires_at
    FROM "Seat";
"""

# Constructs a parameterized SELECT script for optionally including filter 
# Returns both the resulting query and the params
def filter_seats(
        table_id: int | None = None,
        status: SeatStatus | None = None,
        person_id: int | None = None,
        expires_before: datetime | None = None,
        expires_after: datetime | None = None,
):
    query = 'SELECT * FROM "Seat" WHERE 1=1'
    params = []

    if table_id is not None:
        query += " AND table_id = %s"
        params.append(table_id)

    if status is not None:
        query += " AND status = %s"
        params.append(status)

    if person_id is not None:
        query += " AND person_id = %s"
        params.append(person_id)

    if expires_before is not None:
        query += " AND expires_at < %s"
        params.append(expires_before)

    if expires_after is not None:
        query += " AND expires_at > %s"
        params.append(expires_after)

    return query, params

occupy_seat_sql = """
    UPDATE "Seat"
    SET status = 'occupied',
        person_id = %s,
        expires_at = now() + make_interval(secs => %s)
    WHERE id = %s
    RETURNING id, table_id, status, person_id, expires_at;
"""

free_seat_sql = """
    UPDATE "Seat"
    SET status = 'free',
        person_id = NULL,
        expires_at = NULL
    WHERE id = %s
    RETURNING id, table_id, status, person_id, expires_at
"""

free_expired_seats_sql = """
    UPDATE "Seat"
    SET status = 'free', person_id = NULL, expires_at = NULL
    WHERE status = 'occupied' AND expires_at < now()
    RETURNING id, table_id, status, person_id, expires_at;
"""

random_occupied_seat = """
    SELECT id 
    FROM "Seat" 
    WHERE status = 'occupied' 
    ORDER BY RANDOM() 
    LIMIT 1;
"""

unoccupied_seats = """
    SELECT id 
    FROM "Seat" 
    WHERE status = 'free';
"""

all_seats = """
    SELECT *
    FROM "Seat";
"""
