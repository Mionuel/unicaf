import psycopg
from psycopg.rows import dict_row

db_config = {
    "host": "db",
    "dbname": "unicaf-db",
    "user": "admin",
    "password": "pass"
}

def get_db():
    with psycopg.connect(**db_config, row_factory=dict_row) as conn:
        yield conn    
