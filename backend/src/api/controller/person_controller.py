from typing import List

from fastapi import APIRouter, Depends

from db import get_db

from api.view.person_view import new_person
from api.view.person_view import all_people
from api.model.person_model import PersonCreate, PersonResponse

router = APIRouter(
    prefix="/people",
    tags=["People"]
)

@router.get("/all", response_model=List[PersonResponse])
def fetch_all_people(db=Depends(get_db)):
    people = db.execute(
        all_people
    ).fetchall()
    return people

@router.post("/new")
def create_person(person: PersonCreate, db=Depends(get_db)):
    """Creates a new person"""
    db.execute(
        new_person, 
        (person.name, person.initial_credit)
    )
