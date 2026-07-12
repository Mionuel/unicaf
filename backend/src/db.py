import psycopg

from config.db_config import db_config

with psycopg.connect(**db_config) as conn:
    version = conn.execute("SELECT version ()").fetchone()
    print(version)
