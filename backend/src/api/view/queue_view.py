# ON CONFLICT prevents the DBMS from 
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

queue_entries_sql = """
    SELECT id, person_id, joined_at
    FROM "QueueEntry"
    ORDER BY joined_at;
"""

person_already_in_queue = """
    SELECT id 
    FROM "QueueEntry" 
    WHERE person_id = %s
"""

queue_count_sql = """
    SELECT COUNT(*) 
    FROM "QueueEntry";
"""
