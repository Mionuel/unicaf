import psycopg
from config.db_config import db_config

def seed_database():
    with psycopg.connect(**db_config) as conn:
        # create the Person table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Person (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                credit DOUBLE PRECISION DEFAULT 0.0
            )
        """)


if __name__ == "__main__":
    seed_database()
