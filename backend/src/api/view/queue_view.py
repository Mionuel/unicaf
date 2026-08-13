enqueue_sql = """
    INSERT INTO "QueueEntry" (person_id)
    VALUES (%s)
    RETURNING id, person_id, joined_at;
"""

dequeue_sql = """
    DELETE FROM "QueueEntry"
    WHERE id = (
        SELECT id FROM "QueueEntry"
        ORDER BY joined_at
        LIMIT 1
    )
    RETURNING id, person_id, joined_at;
"""
