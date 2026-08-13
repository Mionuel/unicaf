from fastapi import APIRouter, Depends

from api.view.table_view import fetch_table_count

from api.model.table_model import TableCountResponse
from config.db_config import get_db

router = APIRouter(
    prefix="/table",
    tags=["Tables"]
)

@router.get("/", response_model=TableCountResponse)
def get_table_count(db=Depends(get_db)):
    """Fetches the number of tables"""
    result = db.execute(
        fetch_table_count
    ).fetchone()

    return result
