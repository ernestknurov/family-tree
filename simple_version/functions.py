import locale
import streamlit as st
from datetime import datetime


# GET
def get_person_from_db(name: str, surname: str, db: list, patronymic: str=None, match_type: str='all') -> dict:
    """Return persons which names or surnames match with given names"""
    matches = []
    if match_type == 'all':
        for person in db:
                # print(f"Name: {name}; Name type: {type(name)}")
                # print(f"Surname: {surname}; Surname type: {type(surname)}")
                if (not name or name.lower() in person['name'].lower()) and \
                    (not surname or surname.lower() in person['surname'].lower()) and \
                    (not patronymic or patronymic.lower() in person['patronymic'].lower()):
                    matches.append(person)
    elif match_type == 'exact':
        for person in db:
            if (name.lower() == person['name'].lower()) and \
                (surname.lower() == person['surname'].lower()) and \
                (not patronymic or patronymic.lower() == person['patronymic'].lower()):
                matches.append(person)
    else:
        raise Exception("Invalid match_type. Possible values are ['all', 'exact']")

    return matches

def get_person_from_db_by_id(id: int,  db: list) -> dict:
    for person in db:
        if person['id'] == id:
            return person
    return {}

def get_person_id_from_full_name(full_name: str, persons: list) -> int:
    split = full_name.split()
    if len(split) == 3:
        surname, name, patronymic = split
        matches = get_person_from_db(name, surname, persons, patronymic=patronymic, match_type='exact')
    elif len(split) == 2:
        # assuming that surname comes first, then name
        surname, name = split
        matches = get_person_from_db(name, surname, persons, match_type='exact')
    
    if not len(matches):
        raise Exception("No matches were found")
    return matches[0]['id']


def get_person_full_name_from_id(id: int, db: list) -> str:
    person = get_person_from_db_by_id(id, db)
    full_name = " ".join([person[field] for field in ['surname', 'name', 'patronymic'] if person[field]])
    return full_name


def get_person_full_name(person: dict) -> str:
    full_name = " ".join([person[field] for field in ['surname', 'name', 'patronymic'] if person[field]])
    return full_name


# DELETE
def delete_person_from_db(person: dict, db: list) -> bool:

    def delete_links(from_whom: str, whom: str, person: dict=person, db: list=db) -> bool:
        if isinstance(person['links'][from_whom], list):
            for relative_id in person['links'][from_whom]:
                relative_id_in_list = [relative_id == person['id'] for person in db].index(True)
                if isinstance(person['links'][whom], list):
                    db[relative_id_in_list]['links'][whom].remove(person['id'])
                elif isinstance(person['links'][whom], int):
                    db[relative_id_in_list]['links'][whom] = None
        elif isinstance(person['links'][from_whom], int):
            relative_id = person['links'][from_whom]
            relative_id_in_list = [relative_id == person['id'] for person in db].index(True)
            if isinstance(person['links'][whom], list):
                db[relative_id_in_list]['links'][whom].remove(person['id'])
            elif isinstance(person['links'][whom], int):
                db[relative_id_in_list]['links'][whom] = None
        return True
    
    delete_links('mother', 'childs')
    delete_links('father', 'childs')
    delete_links('childs', 'father' if person['is_male'] else 'mother')
    delete_links('siblings', 'siblings')
    delete_links('partners', 'partners')
    db.remove(person)
    return True



# ADD
def add_person_to_db(person: dict, db: dict) -> bool:

    def add_links(from_whom: str, whom: str, person: dict=person, db: list=db) -> bool:
        if isinstance(person['links'][from_whom], list):
            for relative_id in person['links'][from_whom]:
                relative_id_in_list = [relative_id == person['id'] for person in db].index(True)
                if isinstance(person['links'][whom], list):
                    db[relative_id_in_list]['links'][whom].append(person['id'])
                elif isinstance(person['links'][whom], int):
                    db[relative_id_in_list]['links'][whom] = person['id']
        elif isinstance(person['links'][from_whom], int):
            relative_id = person['links'][from_whom]
            relative_id_in_list = [relative_id == person['id'] for person in db].index(True)
            if isinstance(person['links'][whom], list):
                db[relative_id_in_list]['links'][whom].append(person['id'])
            elif isinstance(person['links'][whom], int):
                db[relative_id_in_list]['links'][whom] = person['id']
        return True
    
    person['id'] = max([person['id'] for person in db]) + 1
    add_links('mother', 'childs')
    add_links('father', 'childs')
    add_links('childs', 'father' if person['is_male'] else 'mother')
    add_links('siblings', 'siblings')
    add_links('partners', 'partners')
    db.append(person)
    return True



# OTHER
def beautify_person_info(person: dict, db: list) -> dict:
    
    locale.setlocale(locale.LC_TIME, 'ru_RU.utf8')
    beautified_person = {}
    
    # map fields to readble russian
    beautified_person['ФИО'] = get_person_full_name_from_id(person['id'], db)
    if not person['is_male']:
        beautified_person['Девичья фамилия'] = person['maiden_name']
    beautified_person['Пол'] = 'мужчина' if person['is_male'] else 'женщина'
    beautified_person['Дата рождения'] = person['date_of_birth']
    beautified_person['Дата смерти'] = person['date_of_death']
    beautified_person['Неформальная роль'] = person['informal_role']
    beautified_person['Место рождения'] = person['place_of_birth']
    beautified_person['Место проживания'] = person['place_of_residance']
    beautified_person['Образование'] = person['education']
    beautified_person['Занятость'] = person['occupation']
    beautified_person['Родственники'] = {
        'Отец': get_person_full_name_from_id(person['links']['father'], db) if person['links']['father'] is not None else None,
        'Мать': get_person_full_name_from_id(person['links']['mother'], db) if person['links']['mother'] is not None else None,
        'Братья/сёстры': ", ".join([get_person_full_name_from_id(sib, db) for sib in person['links']['siblings']]) if person['links']['siblings'] is not None else None,
        'Дети': ", ".join([get_person_full_name_from_id(ch, db) for ch in person['links']['childs']]) if person['links']['childs'] is not None else None,
        'Супруги': ", ".join([get_person_full_name_from_id(pt, db) for pt in person['links']['partners']]) if person['links']['partners'] is not None else None
    }
    beautified_person['Контакты'] = person['contacts']
    beautified_person['Другое'] = person['notes']


    if beautified_person['Дата рождения']:
        beautified_person['Дата рождения'] = datetime.strptime(beautified_person['Дата рождения'], '%Y-%m-%d')
    if beautified_person['Дата смерти']:
        beautified_person['Дата смерти'] = datetime.strptime(beautified_person['Дата смерти'], '%Y-%m-%d')

    final_info = ''
    for key, value in beautified_person.items():
        if value is None:
            final_info += f"**{key}**: \-  \n"
        elif isinstance(value, datetime):
            final_info += f"**{key}**: {value.strftime('%d %B %Y')}  \n"
        elif isinstance(value, dict):
            final_info += f'**{key}**:  \n'
            for inner_key, inner_value in value.items():
                if inner_value is None or inner_value == []:
                    final_info += f"* {inner_key}: \-  \n"
                else:
                    final_info += f'* {inner_key}: {inner_value}  \n'
            final_info += "\n"
        else:
            final_info += f"**{key}**: {value}  \n"
    print(final_info)
    return final_info


