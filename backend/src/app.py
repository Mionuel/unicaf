import asyncio
import contextlib
import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.controller.person_controller import router as people_router
from api.controller.table_contoller import router as table_router
from api.controller.seat_controller import router as seat_router
from api.controller.reservation_controller import router as reservation_router
from api.controller.queue_controller import router as queue_router
from api.controller.simulation_controller import router as state_router
from api.controller.socket_controller import broadcast_state, router as socket_router

from config.db_config import get_db
from config.logging_config import setup_logging

from api.controller.simulation_controller import simulate_step, update_all_seats
from api.model.simulation_model import SeedRequest, SimulationResponse, SimulationStatus

import structlog

from db.seed import seed_database
from config.app_config import SimulationSettings, app_settings

_LOGGER = structlog.get_logger()

# Reads the JSON_LOGS env variable, if not set => false
json_env = os.getenv("JSON_LOGS", "false").lower()

setup_logging(json_env == "true")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(people_router)
app.include_router(table_router)
app.include_router(seat_router)
app.include_router(reservation_router)
app.include_router(queue_router)
app.include_router(state_router)
app.include_router(socket_router)

IS_SIMULATION_RUNNING = False

@app.get("/")
def home():
    return {"message": "Hello, UniCaf!"}

async def simulation_loop():
    global IS_SIMULATION_RUNNING
    
    db_context = contextlib.contextmanager(get_db)
    
    while IS_SIMULATION_RUNNING:
        try:
            # With block opens the connection and automatically closes it when not needed
            with db_context() as db:
                simulate_step(db)
                update_all_seats(db)
                await broadcast_state(db)

        except Exception as e:
            _LOGGER.error(
                "simulation_loop_error",
                error=str(e),
            )

        # Wait before next simulation step 
        await asyncio.sleep(app_settings.simulation_interval)


@app.post("/start")
async def start_simulation():
    global IS_SIMULATION_RUNNING

    response = SimulationResponse(
        status=SimulationStatus.running,
        message="Simulation started"
    )
    
    if IS_SIMULATION_RUNNING:
        response.message="Simulation is already running"
        # The return here prevents from creating another simulation loop
        return response

    IS_SIMULATION_RUNNING = True

    asyncio.create_task(simulation_loop())
    
    _LOGGER.info(
        "simulation_started"
    )

    return response

@app.post("/stop")
async def stop_simulation():
    global IS_SIMULATION_RUNNING

    response = SimulationResponse(
        status=SimulationStatus.stopped,
        message="Simulation stopped"
    )

    if not IS_SIMULATION_RUNNING:
        response.message="Simulation is already stopped"
    
    IS_SIMULATION_RUNNING = False
    
    _LOGGER.info(
        "simulation_stopped"
    )

    return response


@app.post("/seed")
def seed_db(payload: SeedRequest, db=Depends(get_db)):
    try:
        # RESTART IDENTITY restarts the id auto increments from 0
        db.execute('TRUNCATE TABLE "Person", "Table", "Seat" RESTART IDENTITY CASCADE;')
        db.commit()

        seed_database(payload.peopleTotal, payload.tablesTotal)

        _LOGGER.info(
                "db_seeding_success",
                num_people=payload.peopleTotal,
                num_tables=payload.tablesTotal
        )

    except Exception as e:  
        _LOGGER.error(
            "database_seed_failed",
            error=str(e)
        )
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/settings", response_model=SimulationSettings)
def get_settings():
    """
        Returns the current settings
    """
    return app_settings

@app.put("/settings", response_model=SimulationSettings)
def update_settings(new_settings: SimulationSettings):
    """
        Updates the app's settings
    """
    for key, value in new_settings.model_dump().items():
        setattr(app_settings, key, value)
        
    _LOGGER.info(
        "settings_updated", 
        new_settings=app_settings.model_dump()
    )
    
    return app_settings
