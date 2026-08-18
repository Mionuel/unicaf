import random

import psycopg
from config.db_config import db_config

import structlog

_LOGGER = structlog.get_logger()

# Create y random tables (label should be an integer)
# Create 4 * y random seats per table (all with status free)
def seed_database(
        num_people: int = 1000, 
        num_tables: int = 20, 
        seats_per_table: int = 4
):
    _LOGGER.info(
        "db_seeding_start"
    )

    with psycopg.connect(**db_config) as conn:
        generate_people(conn, num_people)
        generate_tables(conn, num_tables)
        generate_seats(conn, seats_per_table)

    _LOGGER.info(
        "db_seeding_end"
    )

# Generates n random people (random names (selected from a file with first and last names) + credits + bonus)
def generate_people(
        conn,
        n: int, 
        names_path: str = "src/db/names.txt", 
        surnames_path: str = "src/db/surnames.txt"
):
    # Open the files that contain names and surnames
    with open(names_path, "r", encoding="utf-8") as f:
        names = [line.strip() for line in f if line.strip()]

    with open(surnames_path, "r", encoding="utf-8") as f:
        surnames = [line.strip() for line in f if line.strip()]

    # Stores the generated data
    people_data = []
    for _ in range(n):
        name = random.choice(names)
        surname = random.choice(surnames)
        credit = round(random.uniform(0.0, 50.0), 2) # range 0 - 50
        bonus_points = random.randint(0, 10)         # range 0 - 10
        people_data.append((name + " " + surname, credit, bonus_points))

    # for x in people_data:
    #     print(x)

    with conn.cursor() as cur:
        cur.executemany(
            """
            INSERT INTO "Person" (name, credit, bonus_points) 
            VALUES (%s, %s, %s)
            """,
            people_data
        )

    _LOGGER.info(
        "db_seeding_people",
        num_people=n
    )

def generate_tables(conn, n: int):
    with conn.cursor() as cur:
        # Executes 'INSERT INTO "Table" DEFAULT VALUES' n times
        cur.executemany('INSERT INTO "Table" DEFAULT VALUES;', [()] * n)
        
    _LOGGER.info(
        "db_seeding_tables",
        num_tables=n
    )

def generate_seats(conn, seats_per_table: int):
    with conn.cursor() as cur:
        # Fetch all existing table IDs from the "Table" relation
        cur.execute('SELECT id FROM "Table"')
        tables = cur.fetchall()
        
        seats_data = []
        for (table_id,) in tables:
            for _ in range(seats_per_table):
                # (table_id, status, person_id, expires_at)
                seats_data.append((table_id, "free", None, None))
        
        cur.executemany(
            """
            INSERT INTO "Seat" (table_id, status, person_id, expires_at)
            VALUES (%s, %s, %s, %s)
            """,
            seats_data
        )

    _LOGGER.info(
        "db_seeding_seats",
        total_seats=len(seats_data),
        seats_per_table=seats_per_table
    )

if __name__ == "__main__":
    seed_database()
