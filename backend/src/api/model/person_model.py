from pydantic import BaseModel

# Data type for creating a person
class PersonCreate(BaseModel):
    name: str
    init_credit: float = 0.0
    init_bonus: int = 0

# Data type for the response
class PersonResponse(BaseModel):
    id: int
    name: str
    credit: float
    bonus_points: int
