insert_order_sql = """
    INSERT INTO "Order" (person_id, seat_id, cost, bonus_snack)
    VALUES (%s, %s, %s, %s)
"""
