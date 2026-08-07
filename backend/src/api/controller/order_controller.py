from api.view.order_view import insert_order_sql 

ORDER_COST = 10.0

def insert_order(person_id: int, seat_id: int, bonus_snack: bool, db):
    db.execute(insert_order_sql, (person_id, seat_id, ORDER_COST, bonus_snack))
