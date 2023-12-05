def get_person(name: str, surname: str, persons: dict) -> dict:
    """Return persons which names or surnames match with given names"""
    matches = []
    for person in persons:
            # print(f"Name: {name}; Name type: {type(name)}")
            # print(f"Surname: {surname}; Surname type: {type(surname)}")
            if (not name or name.lower() in person['name'].lower()) and \
                (not surname or surname.lower() in person['surname'].lower()):
                matches.append(person)

    return matches