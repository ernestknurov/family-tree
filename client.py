import requests
import json
from datetime import date
from models import Person, PersonUpdate
from pprint import pprint

BASE_URL = "http://127.0.0.1:8000"  # default FastAPI address

template = {
    "id": "",
    "name": "",
    "surname": "",
    "patronymic": "",
    "date_of_birth": "",
    "date_of_death": "",
    "maiden_name": "",
    "informal_role": "",
    "place_of_birth": "",
    "place_of_residance": "",
    "education": "",
    "occupation": "",
    "contacts": {},
    "links": {
        "mother": "",
        "father": "",
        "childs": []
    },
    "notes": ""
}
new_person_dict = {
    "name": "Chilly",
    "surname": "Billy",
    "patronymic": "Milly",
    "date_of_birth": "1987-01-01",
    "date_of_death": ""
}
new_person = PersonUpdate(
    name="Chilly",
    surname="Billy",
)
new_person_dict = new_person.model_dump_json(by_alias=True)
id = ""
response = requests.put(f"{BASE_URL}/person/{id}", data=new_person_dict, headers={"Content-Type": "application/json"})
print(response.status_code)
print(response.json())

response = requests.get(f"{BASE_URL}/person/{id}")
print(response.status_code)
print(response.json())

response = requests.delete(f"{BASE_URL}/person/{id}")
print(response.status_code)
print(response.json())

person = Person(**response.json())
print(person)

response = requests.get(f"{BASE_URL}/person/{id}")
print(response.status_code)
print(response.json())

response = requests.get(f"{BASE_URL}/person/{id}")
print(response.status_code)