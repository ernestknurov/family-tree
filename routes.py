from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Person, PersonUpdate

router = APIRouter()


@router.post("/", response_description="Create a new person", status_code=status.HTTP_201_CREATED, response_model=Person)
def create_person(request: Request, person: Person = Body(...)):
    person = jsonable_encoder(person)
    new_person = request.app.database["Persons_v1"].insert_one(person)
    created_person = request.app.database["Persons_v1"].find_one(
        {"_id": new_person.inserted_id}
    )

    return created_person


@router.get("/", response_description="List all people", response_model=List[Person])
def list_people(request: Request):
    people = list(request.app.database["Persons_v1"].find(limit=100))
    return people


@router.get("/{id}", response_description="Get a single Person by id", response_model=Person)
def find_person(id: str, request: Request):
    if (person := request.app.database["Persons_v1"].find_one({"_id": id})) is not None:
        return person
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person with ID {id} not found")


@router.put("/{id}", response_description="Update a person", response_model=Person)
def update_person(id: str, request: Request, person: PersonUpdate = Body(...)):
    person = {k: v for k, v in person.model_dump().items() if v is not None}
    if len(person) >= 1:
        update_result = request.app.database["Persons_v1"].update_one(
            {"_id": id}, {"$set": person}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person with ID {id} not found")

    if (
        existing_book := request.app.database["Persons_v1"].find_one({"_id": id})
    ) is not None:
        return existing_book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person with ID {id} not found")


@router.delete("/{id}", response_description="Delete a Person")
def delete_person(id: str, request: Request, response: Response):
    delete_result = request.app.database["Persons_v1"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Person with ID {id} not found")
