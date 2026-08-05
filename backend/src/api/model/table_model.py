from pydantic import BaseModel

class TableCountResponse(BaseModel):
    total_tables: int
