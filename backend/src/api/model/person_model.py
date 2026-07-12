from pydantic import BaseModel

# Data type for creating a person
class PersonCreate(BaseModel):
    name: str
    initial_credit: float = 0.0

# Data type for the response
class PersonResponse(BaseModel):
    id: int
    name: str
    credit: float
