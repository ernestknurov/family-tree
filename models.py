import uuid
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, validator


class Person(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    surname: Optional[str] = Field(default=None)
    maiden_name: Optional[str] = Field(default=None)
    patronymic: Optional[str] = Field(default=None)
    date_of_birth: Optional[date] = Field(default=None)
    date_of_death: Optional[date] = Field(default=None)
    informal_role: Optional[str] = Field(default=None)
    place_of_birth: Optional[str] = Field(default=None)
    place_of_residance: Optional[str] = Field(default=None)
    education: Optional[str] = Field(default=None)
    occupation: Optional[str] = Field(default=None)
    contacts: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)

    @validator('id', pre=True, always=True)
    def convert_id_to_str(cls, v):
        return str(v)
    
    class Config:
        populate_by_name = True
        json_encoders = {
            uuid.uuid4: lambda o: str(o),
            date: lambda d: d.strftime("%Y-%m-%d") if d else None,
        }
        json_schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Владимир",
                "surname": "Владимов",
                "patronymic": "Владимирович",
                "date_of_birth": date(2023, 1, 1),
                "date_of_death": None
            }
        }



class PersonUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    patronymic: str | None = None
    date_of_birth: date | None = None
    date_of_death: date | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Иван",
                "surname": "Иванов",
                "patronymic": None,
                "date_of_birth": None,
                "date_of_death": date(2021, 1, 1)
            }
        }