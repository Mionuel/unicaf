import psycopg
from psycopg.rows import dict_row

from config.db_config import db_config

def get_db():
    with psycopg.connect(**db_config, row_factory=dict_row) as conn:
        yield conn    
