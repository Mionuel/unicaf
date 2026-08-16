import os

from fastapi import FastAPI, Depends

from api.controller.person_controller import router as people_router
from api.controller.table_contoller import router as table_router
from api.controller.seat_controller import router as seat_router
from api.controller.reservation_controller import router as reservation_router
from api.controller.queue_controller import router as queue_router
from api.controller.simulation_controller import router as state_router

from config.db_config import get_db
from config.logging_config import setup_logging

# Reads the JSON_LOGS env variable, if not set => false
json_env = os.getenv("JSON_LOGS", "false").lower()

setup_logging(json_env == "true")

app = FastAPI()

app.include_router(people_router)
app.include_router(table_router)
app.include_router(seat_router)
app.include_router(reservation_router)
app.include_router(queue_router)
app.include_router(state_router)

@app.get("/")
def home():
    return {"message": "Hello, UniCaf!"}

@app.get("/version")
def db_version(conn=Depends(get_db)):
    version = conn.execute("SELECT version()").fetchone()
    return {"postgres_version": version}
