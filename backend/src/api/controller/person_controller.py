from typing import List

from fastapi import APIRouter, Depends, HTTPException

from config.db_config import get_db

from api.view.person_view import new_person, get_person_by_id, all_people
from api.model.person_model import PersonCreate, PersonResponse

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
def fetch_person(person_id: int, db=Depends(get_db)):
    """Fetches a person with id=person_id"""
    person = db.execute(
        get_person_by_id,
        [person_id]
    ).fetchone()

    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    return person
