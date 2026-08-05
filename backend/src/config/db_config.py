import psycopg
from psycopg.rows import dict_row

db_config = {
    "host": "db",
    "dbname": "unicaf-db",
    "user": "admin",
    "password": "pass"
}

# Establishes a connection with the db
def get_db():
    with psycopg.connect(**db_config, row_factory=dict_row) as conn:
        yield conn   

# Reads a .sql file as a string and runs it wia psycopg
def run_sql(file_path: str):
    with open(file_path) as f:
        sql_script = f.read()

    with psycopg.connect(**db_config) as conn:
        conn.execute(sql_script)
