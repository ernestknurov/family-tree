import requests
import json
from datetime import date
from models import Person, PersonUpdate
from pprint import pprint

BASE_URL = "http://127.0.0.1:8000"  # default FastAPI address, adjust if different

# Sample data to be posted
# person_obj = Person(
#     {
#                 "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
#                 "name": "Эрнест",
#                 "surname": "Кнуров",
#                 "patronymic": "Владимирович",
#                 "date_of_birth": date(2002, 9, 11),
#                 "date_of_death": None
#             }
# )
# person_obj = Person(
#     name="Micheal",
#     surname="Doe",
#     patronymic="Smith",
#     date_of_birth=date(1990, 1, 1)
# )
# person_dict = person_obj.model_dump_json(by_alias=True)

# response = requests.post(f"{BASE_URL}/person", data=person_dict, headers={"Content-Type": "application/json"})
# print(response.status_code)
# print(response.json())
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
response = requests.put(f"{BASE_URL}/person/f014001a-7890-4fe0-9fbb-431d1613452b", data=new_person_dict, headers={"Content-Type": "application/json"})
print(response.status_code)
print(response.json())

response = requests.get(f"{BASE_URL}/person/f014001a-7890-4fe0-9fbb-431d1613452b")
print(response.status_code)
print(response.json())

# response = requests.delete(f"{BASE_URL}/person/b3d8c701-9024-432e-ba09-4fe38be0df4c")
# print(response.status_code)
# print(response.json())

# person = Person(**response.json())
# print(person)

# response = requests.get(f"{BASE_URL}/person/654a6ea519082539ef7123a4")
# print(response.status_code)
# print(response.json())

response = requests.get(f"{BASE_URL}/person/")
print(response.status_code)