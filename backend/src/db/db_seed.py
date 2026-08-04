import psycopg
from config.db_config import db_config

def seed_database():
    with psycopg.connect(**db_config) as conn:
        # conn.execute()


if __name__ == "__main__":
    seed_database()
