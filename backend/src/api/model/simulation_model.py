from enum import Enum, auto

from pydantic import BaseModel

class SimulationAction(Enum):
    enqueue = auto()
    reserve = auto()

class SimulationStatus(str, Enum):
    running = "running"
    stopped = "stopped"

class SimulationResponse(BaseModel):
    status: SimulationStatus
    message: str
