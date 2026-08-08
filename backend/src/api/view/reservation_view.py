fetch_reservation_by_seat = """
    SELECT id, seat_id, person_id FROM "Reservation" WHERE seat_id = %s;
"""

insert_reservation = """
    INSERT INTO "Reservation" (seat_id, person_id)
    VALUES (%s, %s)
    RETURNING id, seat_id, person_id;
"""
