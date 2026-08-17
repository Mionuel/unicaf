from typing import List

from fastapi import APIRouter, Depends, HTTPException

from config.db_config import get_db

from api.view.person_view import new_person, get_person_by_id, all_people, update_person, random_person
from api.model.person_model import PersonCreate, PersonResponse

import structlog

_LOGGER = structlog.get_logger()

BONUS_THRESHOLD = 5

router = APIRouter(
    prefix="/people",
    tags=["People"]
)

@router.get("/", response_model=List[PersonResponse])
def fetch_all_people(db=Depends(get_db)):
    """Fetches all people"""
    people = db.execute(
        all_people
    ).fetchall()
    return people

@router.post("/", response_model=PersonResponse)
def create_person(person: PersonCreate, db=Depends(get_db)):
    """Creates a new person"""
    created_person = db.execute(
        new_person, 
        (person.name, person.init_credit, person.init_bonus)
    ).fetchone()

    if created_person is None:
        raise HTTPException(status_code=400, detail="Could not create person")

    return created_person

@router.get("/{person_id}", response_model=PersonResponse)
def get_person(person_id: int, db=Depends(get_db)):
    """Fetches a person with id=person_id"""
    person = db.execute(
        get_person_by_id,
        [person_id]
    ).fetchone()

    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    return person

# A helper function for querying the DB directly
def fetch_person(person_id: int, db) -> PersonResponse:
    row = db.execute(
        get_person_by_id, 
        [person_id]
    ).fetchone()

    if row is None:
        _LOGGER.warning(
            "person_not_found",
            person_id=person_id
        )
        raise ValueError("Person not found")

    # **row unpacks the dictionary into a PersonResponse object 
    person = PersonResponse(**row)

    _LOGGER.info(
        "person_lookup",
        person_id=person.id
    )
    
    return person

# A helper function for subtracting the credits from a person
# Also checks if the person can have a bonus snack
def subtract_credits(person_id: int, cost: float, db) -> bool:
    person = fetch_person(person_id, db)

    if person.credit < cost:
        _LOGGER.warning(
            "insufficient_credits",
            person_id=person.id,
            credits=person.credit,
            cost=cost
        )
        raise ValueError("Insufficient credits")

    bonus_snack = person.bonus_points >= BONUS_THRESHOLD
    # if the person gets a bonus snack => no bonus points
    new_points = 0 if bonus_snack else person.bonus_points + 1

    db.execute(
        update_person,
        (cost, new_points, person_id),
    )

    _LOGGER.info(
        "credits_subtracted",
        from_person_id=person.id,
        amount_subtracted=cost,
        old_credits=person.credit,
        current_credits=person.credit - cost,
        bonus_points=new_points
    )

    return bonus_snack

# fetches a random person
def fetch_random_person(db) -> int:
    row = db.execute(
        random_person
    ).fetchone()

    if not row:
        _LOGGER.error(
            "empty_people_table"
        )
        raise ValueError("No people exist to simulate with")

    _LOGGER.info(
        "radom_person_selected",
        person_id = row["id"]
    )

    return row["id"]
